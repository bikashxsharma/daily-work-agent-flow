#!/usr/bin/env python3.11
"""Behavioral tests use disposable Git repositories, never company repositories."""
import argparse
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from artifact import initialize, save
from install import install, links
from workflow import build_command, context


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='daily-work-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / 'repo with spaces'
        self.repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True).strip()

    def test_local_exclusion_is_idempotent_and_code_stays_visible(self):
        (self.repo / '.gitignore').write_text('node_modules/\n')
        initialize(self.repo)
        initialize(self.repo)
        exclude = self.repo / '.git/info/exclude'
        self.assertEqual(exclude.read_text().count('/.ai-workflow/'), 1)
        save(self.repo, 'feature', 'plan', '# Proposed\n')
        (self.repo / 'application.py').write_text('print(1)\n')
        self.assertNotIn('.ai-workflow', self.git('status', '--short'))
        self.assertIn('application.py', self.git('status', '--short'))
        self.assertEqual((self.repo / '.gitignore').read_text(), 'node_modules/\n')

    def test_tracked_workflow_refused_without_exclude_change(self):
        (self.repo / '.ai-workflow').mkdir()
        (self.repo / '.ai-workflow/draft.md').write_text('original')
        self.git('add', '.ai-workflow/draft.md')
        before = (self.repo / '.git/info/exclude').read_bytes()
        with self.assertRaises(ValueError):
            initialize(self.repo)
        self.assertEqual(before, (self.repo / '.git/info/exclude').read_bytes())

    def test_original_drafts_and_existing_artifacts_preserved(self):
        target = save(self.repo, 'feature', 'plan', 'first')
        with self.assertRaises(ValueError):
            save(self.repo, 'feature', 'plan', 'second')
        with self.assertRaises(ValueError):
            save(self.repo, 'feature', 'draft', 'modified')
        self.assertEqual(target.read_text(), 'first')

    def test_next_plan_versions_without_overwrite(self):
        first = save(self.repo, 'feature', 'plan', 'first', use_next=True)
        second = save(self.repo, 'feature', 'plan', 'second', use_next=True)
        third = save(self.repo, 'feature', 'plan', 'third', use_next=True)
        self.assertEqual([first.name, second.name, third.name], ['plan.md', 'plan-2.md', 'plan-3.md'])
        self.assertEqual(first.read_text(), 'first')
        self.assertEqual(second.read_text(), 'second')

    def test_path_escape_and_symlinks_refused(self):
        for slug in ('../escape', '/tmp/escape', 'a/b', ''):
            with self.assertRaises(ValueError):
                save(self.repo, slug, 'plan', 'bad')
        (self.repo / '.ai-workflow').symlink_to(self.base, target_is_directory=True)
        with self.assertRaises(ValueError):
            initialize(self.repo)
        self.assertFalse((self.base / 'features').exists())

    def test_nested_artifact_symlink_refused(self):
        directory = initialize(self.repo)
        (directory / 'features').symlink_to(self.base, target_is_directory=True)
        with self.assertRaises(ValueError):
            save(self.repo, 'escaped', 'review', 'bad')
        self.assertFalse((self.base / 'escaped').exists())

    def test_existing_exclusion_preserved(self):
        self.git('config', 'core.excludesFile', str(self.base / 'global-ignore'))
        (self.base / 'global-ignore').write_text('.ai-workflow/\n')
        exclude = self.repo / '.git/info/exclude'
        before = exclude.read_bytes()
        initialize(self.repo)
        self.assertEqual(before, exclude.read_bytes())

    def test_partial_ignore_does_not_expose_artifacts(self):
        (self.repo / '.gitignore').write_text('.ai-workflow/.probe\n')
        save(self.repo, 'feature', 'plan', 'proposed')
        self.assertNotIn('.ai-workflow', self.git('status', '--short'))

    def test_repository_negation_fails_closed(self):
        (self.repo / '.gitignore').write_text('!/.ai-workflow/\n')
        with self.assertRaises(ValueError):
            save(self.repo, 'feature', 'plan', 'proposed')
        self.assertFalse((self.repo / '.ai-workflow/features/feature/plan.md').exists())

    def test_documented_cli_option_order(self):
        script = Path(__file__).resolve().parent / 'workflow.py'
        result = subprocess.run(['python3.11', str(script), 'plan', '--repo', str(self.repo),
                                 '--exec', '--dry-run', 'Task'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--sandbox read-only', result.stdout)
        for flags in (['--verbose', '--write-plan', '--auto-implement'],
                      ['--auto-implement', '--verbose', '--write-plan']):
            result = subprocess.run(['python3.11', str(script), 'delivery', *flags,
                                     '--repo', str(self.repo), '--dry-run', 'Task'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('$feature-delivery --auto-implement --write-plan --verbose Task', result.stdout)
            self.assertIn('Verbose reporting is enabled', result.stdout)

    def test_routing_from_subdirectory_and_personal_fallback(self):
        sub = self.repo / 'src'
        sub.mkdir()
        (self.repo / 'README.md').write_text('personal')
        info = context(sub)
        self.assertEqual(info['root'], str(self.repo))
        self.assertIsNone(info['knowledge_base'])
        self.assertIn('README.md', info['documentation_candidates'])
        (self.repo / 'documents').mkdir()
        (self.repo / 'documents/documents-knowledge-base.md').write_text('index')
        self.assertTrue(context(sub)['knowledge_base'].endswith('documents-knowledge-base.md'))

    def test_installer_idempotence_conflict_and_owned_uninstall(self):
        pairs = links(self.base, self.base / '.codex')
        with contextlib.redirect_stdout(io.StringIO()):
            install(pairs, apply=True)
            install(pairs, apply=True)
        self.assertTrue(all(target.resolve() == source for source, target in pairs))
        with contextlib.redirect_stdout(io.StringIO()):
            install(pairs, apply=True, uninstall=True)
        self.assertFalse(any(target.is_symlink() for _, target in pairs))
        conflict = pairs[-1][1]
        conflict.write_text('existing config')
        with self.assertRaises(ValueError):
            install(pairs, apply=True)
        self.assertFalse(pairs[0][1].exists())
        self.assertEqual(conflict.read_text(), 'existing config')

    def test_launch_boundaries_and_literal_prompt(self):
        args = argparse.Namespace(phase='plan', repo=self.repo, auto_implement=False,
                                  write_plan=False, verbose=False, allow_mcp=[],
                                  task='draft.md; $(touch unsafe)', exec=True)
        cmd = build_command(args, {'mcp_servers': {'new-server': {}}})
        self.assertEqual(cmd[cmd.index('--model') + 1], 'gpt-6-astra')
        self.assertIn('model_reasoning_effort="high"', cmd)
        self.assertEqual(cmd[cmd.index('--sandbox') + 1], 'read-only')
        self.assertIn('approval_policy="never"', cmd)
        self.assertIn('mcp_servers."new-server".enabled=false', cmd)
        self.assertIn('draft.md; $(touch unsafe)', cmd[-1])
        self.assertEqual(cmd[cmd.index('--cd') + 1], str(self.repo))
        args.exec = False
        readonly_plan = build_command(args, {})
        self.assertEqual(readonly_plan[readonly_plan.index('--sandbox') + 1], 'read-only')
        self.assertNotIn('scripts/artifact.py save', readonly_plan[-1])
        args.write_plan = True
        coordinator = build_command(args, {})
        self.assertEqual(coordinator[coordinator.index('--sandbox') + 1], 'workspace-write')
        self.assertIn('scripts/artifact.py save --feature <slug> --kind plan --next', coordinator[-1])
        self.assertIn('do not modify application code', coordinator[-1])
        args.write_plan = False
        args.phase = 'discovery'
        discovery = build_command(args, {})
        self.assertEqual(discovery[discovery.index('--model') + 1], 'gpt-6.1-sol')
        self.assertIn('model_reasoning_effort="medium"', discovery)
        self.assertEqual(discovery[discovery.index('--sandbox') + 1], 'read-only')
        args.phase = 'plan'
        args.auto_implement = True
        cmd = build_command(args, {})
        self.assertEqual(cmd[cmd.index('--sandbox') + 1], 'workspace-write')
        self.assertIn('$feature-plan --auto-implement', cmd[-1])
        args.phase = 'review'
        with self.assertRaises(ValueError):
            build_command(args, {})

    def test_verbose_reporting_and_explicit_mcp_opt_in(self):
        args = argparse.Namespace(phase='quick-fix', repo=self.repo, auto_implement=False,
                                  write_plan=False, verbose=True, allow_mcp=['sentry'],
                                  task='Fix it', exec=False)
        effective = {'mcp_servers': {'sentry': {}, 'atlassian': {}}}
        cmd = build_command(args, effective)
        self.assertIn('$quick-fix --verbose Fix it', cmd[-1])
        self.assertIn('mcp_servers."sentry".enabled=true', cmd)
        self.assertIn('mcp_servers."atlassian".enabled=false', cmd)
        self.assertIn('model gpt-6-luna and reasoning effort medium', cmd[-1])
        args.allow_mcp = ['missing']
        with self.assertRaises(ValueError):
            build_command(args, effective)
        args.allow_mcp = []
        args.write_plan = True
        with self.assertRaises(ValueError):
            build_command(args, effective)

    def test_linked_worktree_exclusion_without_commit(self):
        # Modern Git supports an orphan worktree; skip on older versions.
        worktree = self.base / 'linked'
        result = subprocess.run(['git', '-C', str(self.repo), 'worktree', 'add', '--orphan',
                                 '-b', 'test-worktree', str(worktree)], capture_output=True)
        if result.returncode:
            self.skipTest('Installed Git lacks orphan worktree support')
        initialize(worktree)
        self.assertTrue((worktree / '.git').is_file())
        save(worktree, 'feature', 'specification', 'proposed')
        status = subprocess.check_output(['git', '-C', str(worktree), 'status', '--short'], text=True)
        self.assertNotIn('.ai-workflow', status)


if __name__ == '__main__':
    unittest.main(verbosity=2)

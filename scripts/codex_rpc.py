"""Small stdio client for local Codex capability checks; never starts a model turn."""
import json
import queue
import subprocess
import threading


class Client:
    def __init__(self, options=(), cwd=None):
        self.process = subprocess.Popen(
            ['codex', *options, 'app-server'], cwd=cwd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
        )
        self.messages = queue.Queue()
        self.errors = []
        self.sequence = 0
        threading.Thread(target=self._read, daemon=True).start()
        threading.Thread(target=self._errors, daemon=True).start()
        try:
            self.call('initialize', {'clientInfo': {'name': 'daily-work-setup', 'version': '1'}})
            self.send({'method': 'initialized', 'params': {}})
        except Exception:
            self.close()
            raise

    def _read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                pass
        self.messages.put(None)

    def _errors(self):
        for line in self.process.stderr:
            self.errors.append(line.rstrip())

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + '\n')
        self.process.stdin.flush()

    def call(self, method, params, timeout=30):
        self.sequence += 1
        request_id = self.sequence
        self.send({'id': request_id, 'method': method, 'params': params})
        while True:
            try:
                message = self.messages.get(timeout=timeout)
            except queue.Empty:
                raise RuntimeError(f'Codex timed out on {method}') from None
            if message is None:
                raise RuntimeError('Codex app-server exited: ' + '\n'.join(self.errors[-4:]))
            if message.get('id') == request_id:
                if 'error' in message:
                    raise RuntimeError(f'{method}: {message["error"]}')
                return message['result']

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

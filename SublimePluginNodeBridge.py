import sublime, sublime_plugin, subprocess, threading, json

class NodeBridgeCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    args = [
      sublime.load_settings("SublimePluginNodeBridge.sublime-settings").get("node_path"),
      sublime.packages_path() + "/sublime-plugin-node-bridge/index.js",
      json.dumps({"data":"data for node app"})
    ]

    thread = NodeJS(args)
    thread.start()
    self.handle_thread(thread)

  def handle_thread(self, thread):
    if (thread.isAlive()):
      sublime.set_timeout(lambda: self.handle_thread(thread), 100)
    elif (thread.result != False):
      self.show_result(thread.result)

  def show_result(self, result):
    print(result)

class NodeJS(threading.Thread):

  def __init__(self, args):
    self.args = args
    self.result = None
    threading.Thread.__init__(self)

  def run(self):
    try:
      process = subprocess.Popen(self.args,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        universal_newlines=True)

      # Make the result accessible by the main thread
      self.result = process.communicate()[0]

    except OSError:
      sublime.error_message("Error calling NodeJS app")
      self.result = False
import subprocess
import webbrowser
import qrcode


def publish():

    # Github
    subprocess.run(['git', 'add', 'html/logo.html'])
    subprocess.run(['git', 'commit', '-m', 'Update html.'])
    subprocess.run(['git', 'push'])

    # Generate url
    com = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8')[:-1]
    url = f'https://htmlpreview.github.io/?https://github.com/RobinEnjalbert/SimExporterDemo/blob/{com}/html/logo.html'
    webbrowser.open(url)

    # Generate qr-code
    img = qrcode.make(url)
    img.show()
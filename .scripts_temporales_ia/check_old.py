import subprocess
out = subprocess.check_output(['git', 'show', '2267238:v2.html']).decode('utf-8')
start = out.find('id="loginSection"')
print(out[start:start+1000])

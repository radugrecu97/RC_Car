import jenkins.plugins.publish_over_ssh.*

def sshHost = getSSHHost('RPi_Testing')
def host = [host: sshHost.hostname, user: sshHost.username, password: sshHost.password]
sshHost = null
sh("""
    set +x
    sshpass -p "${host.password}" scp -o StrictHostKeyChecking=no ${host.user}@${host.host}:/home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/reports/gtestresults.xml .
    set -x
""")
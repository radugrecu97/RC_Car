import jenkins.plugins.publish_over_ssh.*

@NonCPS
def getSSHHost(name) {
  def found = null
  Jenkins.instance.getDescriptorByType(BapSshPublisherPlugin.Descriptor.class).each{
    it.hostConfigurations.each{host ->
      if (host.name == name) {
        found = host
      }
    }
  }

  found
}

def sshHost = getSSHHost('RPi_Testing')
def host = [host: sshHost.hostname, user: sshHost.username, password: sshHost.password]
sshHost = null
sh("""
    echo "${host.password} ${host.user} ${host.host}"
    set +x
    sshpass -p "${host.password}" scp -o StrictHostKeyChecking=no ${host.user}@${host.host}:/home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/reports/gtestresults.xml .
    set -x
""")
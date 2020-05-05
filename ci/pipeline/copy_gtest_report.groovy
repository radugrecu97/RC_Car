evaluate(new File("../variables.groovy"))

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

def sshHost = getSSHHost("${env.PUB_OVER_SSH_CONF_NAME}")
def host = [host: sshHost.hostname, user: sshHost.username, password: sshHost.password]
sshHost = null
sh("""
    set +x
    sshpass -p "${host.password}" scp -o StrictHostKeyChecking=no ${host.user}@${host.host}:/home/jenkins/jenkins_slave/workspace/${env.PROJECT_NAME}/reports/gtestresults.xml .
    set -x
""")
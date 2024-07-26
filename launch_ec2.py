import subprocess

def launch_ec2_instances(count, group_name):
    # Define the Ansible playbook content dynamically
    playbook_content = f"""
    - hosts: localhost
      gather_facts: false
      vars:
        count: {count}
        group_name: {group_name}
        instance_type: t2.micro
        key_name: your_key_name
        security_group: your_security_group
        subnet_id: your_subnet_id
        ami_id: your_ami_id

      tasks:
        - name: Launch EC2 instances
          ec2_instance:
            name: "instance_{{ item }}"
            instance_type: "{{ instance_type }}"
            key_name: "{{ key_name }}"
            security_groups: ["{{ security_group }}"]
            subnet_id: "{{ subnet_id }}"
            image_id: "{{ ami_id }}"
          with_sequence: start=1 end={{ count }}
          register: ec2_instances

        - name: Add EC2 instances to Ansible inventory
          add_host:
            name: "{{ item.instance.public_ip }}"
            groups: "{{ group_name }}"
          with_items: "{{ ec2_instances.results }}"
    """

    # Write the playbook content to a temporary file
    playbook_file = "/tmp/launch_ec2_playbook.yml"
    with open(playbook_file, "w") as file:
        file.write(playbook_content)

    # Run the Ansible playbook
    subprocess.run(["ansible-playbook", playbook_file])

    # Clean up temporary playbook file
    subprocess.run(["rm", playbook_file])

if __name__ == "__main__":
    # Prompt the user for input
    count = int(input("Enter the number of EC2 instances to launch (1-5): "))
    group_name = input("Enter the group name to add EC2 instances: ")

    # Validate user input
    if 1 <= count <= 5:
        # Launch EC2 instances using Ansible playbook
        launch_ec2_instances(count, group_name)
    else:
        print("Invalid count. Please enter a number between 1 and 5.")

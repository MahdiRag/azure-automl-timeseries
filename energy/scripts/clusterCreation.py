from authentication import ws
from azureml.core.compute import ComputeTarget, ComputeInstance, AmlCompute
from azureml.core.compute_target import ComputeTargetException

def create_compute_instance(ws=None, compute_name=None):
    """Create AML compute instance, mostly to support dev/test work"""
    compute_name = compute_name
    #compute_name = "ci{}".format(ws._workspace_id)[:10]
    # Verify that instance does not exist already
    try:
        instance = ComputeInstance(workspace=ws, name=compute_name)
        print('Found existing instance, use it.')
    except ComputeTargetException:
        compute_config = ComputeInstance.provisioning_configuration(
            vm_size='STANDARD_D3_V2',
            ssh_public_access=False,
            # vnet_resourcegroup_name='<my-resource-group>',
            # vnet_name='<my-vnet-name>',
            # subnet_name='default',
            # admin_user_ssh_public_key='<my-sshkey>'
        )
        instance = ComputeInstance.create(ws, compute_name, compute_config)
    #instance.wait_for_completion(show_output=True)


def create_compute_cluster(workspace=None, compute_name=None):
    """Create AML compute cluster to support production work
    and repeatable experiments."""

    try:
        cpu_cluster = ComputeTarget(workspace=workspace, name=compute_name)
        print('Found existing cluster, use it.')
    except ComputeTargetException:
        # To use a different region for the compute, add a location='<region>' parameter
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                min_nodes=1,
                max_nodes=5)
        cpu_cluster = ComputeTarget.create(workspace, compute_name, compute_config)
    #cpu_cluster.wait_for_completion(show_output=True)


def main():
    """Main operational flow"""
    cluster_name='newcluster1'
    create_compute_cluster(
            workspace=ws, 
            compute_name=cluster_name
            )

if __name__ == "__main__":
    main()

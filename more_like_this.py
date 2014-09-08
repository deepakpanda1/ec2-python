#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import optparse

import boto.ec2


DEFAULT = {
    'region_name': 'us-east-1',
    'aws_access_key_id': None,
    'aws_secret_access_key': None,
    'base_ec2_hostname': None,
    'base_ec2_id': None,
    'hostname': None,
    'override_ami_id': None,
    'override_sg_ids': None,
    'override_subnet': None,
    'override_ebs_optimize': None,
    'override_instance_type': None,
    'override_private_ip': None,
    'override_public_ip': None,
    'override_terminate_protection': None,
    'override_shutdown_behavior': None,
    'userdata': None,
    'log_level': 'INFO'
}


def get_args():

    usage = (
        'Create EC2 instance like "AWS Launch more like this".'
    )
    parser = optparse.OptionParser(usage=usage)

    aws_credential_option_group = optparse.OptionGroup(
        parser,
        'AWS credential parameters'
    )

    aws_credential_option_group.add_option(
        '--region-name', '-r',
        type='string', default=DEFAULT['region_name'],
        dest='region_name',
        help='AWS Region Name.'
    )
    aws_credential_option_group.add_option(
        '--aws-access-key-id', '-i',
        type='string', default=DEFAULT['aws_access_key_id'],
        dest='aws_access_key_id',
        help='AWS Access Key Id'
    )
    aws_credential_option_group.add_option(
        '--aws-secret-access-key', '-k',
        type='string', default=DEFAULT['aws_secret_access_key'],
        dest='aws_secret_access_key',
        help='AWS Secret Access Key'
    )
    parser.add_option_group(aws_credential_option_group)

    override_option_group = optparse.OptionGroup(
        parser,
        'Override Instance Options'
    )

    override_option_group.add_option(
        '--override-ami-id', '-a',
        type='string', default=DEFAULT['override_ami_id'],
        dest='override_ami_id',
        help='When you want to override new instance AMI, use this option.'
    )
    override_option_group.add_option(
        '--override-sg-id', '-s',
        type='string', default=DEFAULT['override_sg_ids'],
        dest='override_sg_id',
        help='when you want to override new instance sgs, use this option.'
    )
    override_option_group.add_option(
        '--override-subnet', '-c',
        type='string', default=DEFAULT['override_subnet'],
        dest='override_subnet',
        help='when you want to override new instance subnet, use this option.'
    )
    override_option_group.add_option(
        '--override-ebs-optimize', '-e',
        type='string', default=DEFAULT['override_ebs_optimize'],
        dest='override_ebs_optimize',
        help=(
            'when you want to override new instance ebs optimize option, '
            'use this option.'
        )
    )
    override_option_group.add_option(
        '--override-instance-type', '-t',
        type='string', default=DEFAULT['override_instance_type'],
        dest='override_instance_type',
        help=(
            'when you want to override new instance instance type, '
            'use this option.'
        )
    )
    override_option_group.add_option(
        '--override-private-ip', '-x',
        type='string', default=DEFAULT['override_private_ip'],
        dest='override_private_ip',
        help=(
            'when you want to override new instance private IP address, '
            'use this option.'
        )
    )
    override_option_group.add_option(
        '--override-public-ip', '-y',
        type='string', default=DEFAULT['override_public_ip'],
        dest='override_instance_type',
        help=(
            'when you want to override new instance public IP option, '
            'use this option.'
        )
    )
    override_option_group.add_option(
        '--override-terminate-protection', '-d',
        type='string', default=DEFAULT['override_terminate_protection'],
        dest='override_terminate_protection',
        help=(
            'When you want to '
            'override new instance terminate protection option, '
            'use this option.'
        )
    )
    override_option_group.add_option(
        '--override-shutdown-behavior', '-b',
        type='string', default=DEFAULT['override_shutdown_behavior'],
        dest='override_shutdown_behavior',
        help=(
            'When you want to override new instance shutdown behavior, '
            'use this option.'
        )
    )
    parser.add_option_group(override_option_group)

    parser.add_option(
        '--base-ec2-name', '-N',
        type='string', default=DEFAULT['base_ec2_hostname'],
        dest='base_ec2_name',
        help='Based EC2 instance hostname.'
    )
    parser.add_option(
        '--base-ec2-id', '-I',
        type='string', default=DEFAULT['base_ec2_id'],
        dest='base_ec2_id',
        help='Based EC2 instance id.'
    )
    parser.add_option(
        '--hostname', '-H',
        type='string', default=DEFAULT['hostname'],
        help='New EC2 instance hostname.'
    )
    parser.add_option(
        '--userdata', '-U',
        type='string', default=DEFAULT['userdata'],
        help='Injected AWS "Userdata".'
    )
    parser.add_option(
        '--log-level', '-L',
        type='choice', default=DEFAULT['log_level'],
        choices=[
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ],
        help=(
            'Injected AWS "Userdata".'
        )
    )

    return parser.parse_args()[0]


class EC2MoreLikeThisException(BaseException):

    def __init__(self, message):
        super(EC2MoreLikeThisException, self).__init__(message)


def validate_options(options):

    if options.aws_access_key_id is None:
        raise EC2MoreLikeThisException(
            '"--aws-access-key-id" option is required.'
        )

    if options.aws_secret_access_key is None:
        raise EC2MoreLikeThisException(
            '"--aws-secret-access-key" option is required.'
        )

def create_conn(region_name, aws_access_key_id, aws_secret_access_key):

    try:
        conn = boto.ec2.connect_to_region(
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    except Exception as exception:
        raise EC2MoreLikeThisException(
            exception.__str__()
        )

    if conn is None:
        raise EC2MoreLikeThisException(
            'Maybe failed to AWS authentication.'
        )

    return conn


if __name__ == '__main__':
    get_args()
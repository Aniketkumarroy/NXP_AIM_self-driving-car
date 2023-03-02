#!/usr/bin/env python3
"""
Generate Models
@author: Benjamin Perseghetti
@email: bperseghetti@rudislabs.com
"""
import jinja2
import argparse
import os
import numpy as np

rel_gazebo_path = ".."
rel_model_path ="../models"
script_path = os.path.realpath(__file__).replace("jinja_model_gen.py","")
default_env_path = os.path.relpath(os.path.join(script_path, rel_gazebo_path))
default_model_path = os.path.relpath(os.path.join(script_path, rel_model_path))
default_sdf_dict = {
    "nxp_cupcar": 1.5
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_model', default="NotSet", help="Base model jinja file EX: iris")
    parser.add_argument('--controller', default="NotSet", help="Controller to use with model")
    parser.add_argument('--sdf_version', default="NotSet", help="SDF format version to use for interpreting model file")
    parser.add_argument('--mavlink_tcp_port', default=4560, help="TCP port for PX4 SITL")
    parser.add_argument('--mavlink_udp_port', default=14560, help="Mavlink UDP port for mavlink access")
    parser.add_argument('--qgc_udp_port', default=14550, help="QGC UDP port")
    parser.add_argument('--sdk_udp_port', default=14540, help="SDK UDP port")
    parser.add_argument('--serial_enabled', default="NotSet", help="Enable serial device for HITL")
    parser.add_argument('--serial_device', default="/dev/ttyACM0", help="Serial device for FMU")
    parser.add_argument('--serial_baudrate', default=921600, help="Baudrate of Serial device for FMU")
    parser.add_argument('--enable_lockstep', default="NotSet", help="Enable lockstep for simulation")
    parser.add_argument('--hq_frame', default=0, help="Enable low poly count on frame")
    parser.add_argument('--hq_wheel', default=0, help="Enable low poly count on wheel")
    parser.add_argument('--pixy2_cmucam5', default=1, help="Enable pixycam")
    parser.add_argument('--camera_image', default="NotSet", help="Name of camera image topic.")
    parser.add_argument('--namespace', default="NotSet", help="Namespace of robot.")
    parser.add_argument('--hil_mode', default=0, help="Enable HIL mode for HITL simulation")
    parser.add_argument('--model_name', default="NotSet", help="Model to be used in jinja files")
    args = parser.parse_args()

    if args.namespace == "":
        args.namespace = "NotSet"

    if args.base_model not in default_sdf_dict:
        print("\nWARNING!!!")
        print('Base model: "{:s}" DOES NOT MATCH any entries in default_sdf_dict.\nTry base model name:'.format(args.base_model))
        for model_option in default_sdf_dict:
            print('\t{:s}'.format(model_option))
        print("\nEXITING jinja_model_gen.py...\n")
        exit(1)

    if args.model_name == "NotSet":
        args.model_name = args.base_model
    
    if args.sdf_version == "NotSet":
        args.sdf_version = default_sdf_dict.get(args.base_model)
        
    input_filename = os.path.relpath(os.path.join(default_model_path, '{:s}/{:s}.sdf.jinja'.format(args.base_model,args.base_model)))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(default_env_path))
    template_model = env.get_template(os.path.relpath(input_filename, default_env_path))
    
    if args.serial_enabled=="NotSet":
        args.serial_enabled=0

    if args.enable_lockstep=="NotSet":
        args.enable_lockstep=1

    d = {'sdf_version': args.sdf_version, \
         'controller': args.controller, \
         'mavlink_tcp_port': args.mavlink_tcp_port, \
         'mavlink_udp_port': args.mavlink_udp_port, \
         'qgc_udp_port': args.qgc_udp_port, \
         'sdk_udp_port': args.sdk_udp_port, \
         'serial_enabled': args.serial_enabled, \
         'serial_device': args.serial_device, \
         'serial_baudrate': args.serial_baudrate, \
         'enable_lockstep': args.enable_lockstep, \
         'model_name': args.model_name, \
         'hq_frame': args.hq_frame, \
         'hq_wheel': args.hq_wheel, \
         'pixy2_cmucam5': args.pixy2_cmucam5, \
         'camera_image': args.camera_image, \
         'namespace': args.namespace, \
         'hil_mode': args.hil_mode}

    if (not os.path.isdir('/tmp/gazebo/models/{:s}'.format(args.model_name))):
        try: 
            os.makedirs('/tmp/gazebo/models/{:s}'.format(args.model_name), exist_ok = True) 
        except OSError as error: 
            print("Directory creation error.")

    model_result = template_model.render(d)
    model_out = '/tmp/gazebo/models/{:s}/{:s}.sdf'.format(args.model_name, args.model_name)

    with open(model_out, 'w') as m_out:
        print(('{:s} -> {:s}'.format(input_filename, model_out)))
        m_out.write(model_result)

    input_config = os.path.relpath(os.path.join(script_path, 'model.config.jinja'))
    template_config = env.get_template(os.path.relpath(input_config, default_env_path))
    result_config = template_config.render(d)
    out_config = '/tmp/gazebo/models/{:s}/model.config'.format(args.model_name)
    with open(out_config, 'w') as c_out:
        print(('{:s} -> {:s}'.format("scripts/model.config.jinja", out_config)))
        c_out.write(result_config)

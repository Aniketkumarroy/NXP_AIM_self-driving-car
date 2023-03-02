#!/usr/bin/env python3
"""
Generate Worlds
@author: Benjamin Perseghetti
@email: bperseghetti@rudislabs.com
"""
import jinja2
import argparse
import os
import numpy as np
import datetime
import ast

rel_gazebo_path = ".."
rel_world_path ="../worlds"
script_path = os.path.realpath(__file__).replace("jinja_world_gen.py","")
default_env_path = os.path.relpath(os.path.join(script_path, rel_gazebo_path))
default_world_path = os.path.relpath(os.path.join(script_path, rel_world_path))
default_filename = os.path.relpath(os.path.join(default_world_path, "gen.world.jinja"))
default_sdf_world_dict = {
    "empty": 1.5,
    "mcmillan": 1.5,
    "ksql": 1.5,
    "irlock": 1.5,
    "boat": 1.5,
    "baylands": 1.5,
    "yosemite": 1.5,
    "windy": 1.5,
    "warehouse": 1.5,
    "typhoon": 1.5,
    "nxp_raceway_overpass": 1.5,
    "nxp_raceway_octagon": 1.5,
    "raceway": 1.5,
    "canvas": 1.5
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdf_version', default="NotSet", help="SDF format version to use for interpreting world file")
    parser.add_argument('--sun_model', default="sunSolarNoon", help="Select sun model [sunSolarNoon, sunHighShadow, sunUTC, sunNone]")
    parser.add_argument('--sun_utc_date', default="1904_09_20_17_30", help="Date 'YYYY_MM_DD_hh_mm' with UTC time to calculate sunUTC values or 'Now' for your current UTC time.")
    parser.add_argument('--cloud_speed', default="NoClouds", help="Turn on clouds with given speed")
    parser.add_argument('--shadows', default=1, help="Shadows on [1] or off [0]")
    parser.add_argument('--video_widget', default="NotSet", help="GUI video widget on [1] or off [0]")
    parser.add_argument('--update_rate', default=250, help="Real time update rate.")
    parser.add_argument('--wind_speed', default="NotSet", help="Turn on wind with given mean speed.")
    parser.add_argument('--fog_params', default="NotSet", help="Dictionary of fog attributes (type, start_m, end_m, density).")
    parser.add_argument('--realtime_factor', default=1.0, help="Real time factor.")
    parser.add_argument('--world_name', default="NotSet", help="Name of world, see default_sdf_world_dict for options")
    parser.add_argument('--ambient_light', default=0.5, help="Value for ambient light [0.0..1.0]")
    parser.add_argument('--background_light', default=0.15, help="Value for background light [0.0..1.0]")
    parser.add_argument('--use_spherical_coords', default="NotSet", help="Enable or disable spherical coordinates on [1] or off [0]")
    parser.add_argument('--lat_lon_alt', default=[39.8039,-84.0606, 244], help="Latitude, Longitude, Altitude for spherical coordinates and sunUTC calculation")
    parser.add_argument('--embedded_models', default="NotSet", help="Array of models with poses to be embedded in world file")
    parser.add_argument('--set_physics', default=1, help="Enable or disable physics in world file, on [1] or off [0]")
    parser.add_argument('--output_file', help="world output file")
    parser.add_argument('--ode_threads', default=2, help="Number of island threads to use for ODE.")
    args = parser.parse_args()

    print('Generation script passed world name: "{:s}"'.format(args.world_name))


    try:
        deg_latitude, deg_lognitude, m_altitude = ast.literal_eval(str(args.lat_lon_alt))
    except:
        print("Failed to read passed lat_lon_alt")
        deg_latitude, deg_lognitude, m_altitude = [39.8039, -84.0606, 244]
        pass

    if args.embedded_models != "NotSet":
        try:
            args.embedded_models = ast.literal_eval(args.embedded_models)
        except:
            print("Failed to read passed embedded_models dictionary")
            args.embedded_models = "NotSet"
            pass

    if args.fog_params != "NotSet":
        try:
            args.fog_params = ast.literal_eval(args.fog_params)
        except:
            print("Failed to read passed fog_params dictionary")
            args.fog_params = "NotSet"
            pass

    if args.world_name not in default_sdf_world_dict:
        print("\nERROR!!!")
        print('World name: "{:s}" DOES NOT MATCH any entries in default_sdf_world_dict.\nTry world name:'.format(args.world_name))
        for world_option in default_sdf_world_dict:
            print('\t{:s}'.format(world_option))
        print("\nEXITING jinja_world_gen.py...\n")
        exit(1)

    if args.sdf_version == "NotSet":
        args.sdf_version = default_sdf_world_dict.get(args.world_name)
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(default_env_path))
    template = env.get_template(os.path.relpath(default_filename, default_env_path))

    if args.sun_model == "sunUTC":
        try:
            import pysolar
        except ImportError:
            print("Failed to import pysolar - try installing with: \n\tsudo apt install python3-pysolar\n")
            args.sun_model = "sunNone"
            pass

    if args.sun_model == "sunUTC":
        dateStringUTC = args.sun_utc_date
        if dateStringUTC == "Now":
            dateUTC = datetime.datetime.now(datetime.timezone.utc)
        else:
            if len(dateStringUTC) != 16:
                dateStringUTC='1904/09/20/17:30'
            YYYY = int(dateStringUTC[:4])
            MM = int(dateStringUTC[5:7])
            DD = int(dateStringUTC[8:10])
            hh = int(dateStringUTC[11:13])
            mm = int(dateStringUTC[14:16])
            dateUTC = datetime.datetime(YYYY, MM, DD, hh, mm, 0, 0, tzinfo=datetime.timezone.utc)
        sunLatitude = float(deg_latitude)
        sunLongitude = float(deg_lognitude)
        sunAzimuth = pysolar.solar.get_azimuth(sunLatitude, sunLongitude, dateUTC)
        sunAltitude = pysolar.solar.get_altitude(sunLatitude, sunLongitude, dateUTC)
        sunRadiation =  pysolar.radiation.get_radiation_direct(dateUTC, sunAltitude)
        if sunRadiation > 1000.0:
            sunRadiation = 1000.0
        if sunRadiation < 0.0:
            sunRadiation = 0.0
        sunRadiationNorm = sunRadiation/1000.0
        specularRatio = 0.3    
        sunDiffuse = '{:1.3f} {:1.3f} {:1.3f} {:1.3f} 1'.format(sunRadiationNorm,sunRadiationNorm,sunRadiationNorm,sunRadiationNorm)
        sunSpecular = '{:1.3f} {:1.3f} {:1.3f} {:1.3f} 1'.format(specularRatio*sunRadiationNorm,specularRatio*sunRadiationNorm,specularRatio*sunRadiationNorm,specularRatio*sunRadiationNorm)
    
        sunAzimuthRad=sunAzimuth*np.pi/180.0
        sunAltitudeRad=sunAltitude*np.pi/180.0
    
        Xenu = -np.cos(sunAltitudeRad)*np.sin(sunAzimuthRad)
        Yenu = -np.cos(sunAltitudeRad)*np.cos(sunAzimuthRad)
        Zenu = -np.sin(sunAltitudeRad)
    
        sunVector = '{:1.3f} {:1.3f} {:1.3f}'.format(Xenu, Yenu, Zenu)
    
        if sunRadiationNorm == 0:
            args.sun_model="sunNight"
    else:
        sunDiffuse="NotSet"
        sunSpecular="NotSet"
        sunVector="NotSet"

    if args.sun_model == "sunNight":
        print("WARNING: WORLD IS SET TO NIGHT TIME MODE!!!")

    d = {'sdf_version': args.sdf_version, \
         'sun_model': args.sun_model, \
         'sun_diffuse': sunDiffuse, \
         'sun_specular': sunSpecular, \
         'sun_vector': sunVector, \
         'cloud_speed': args.cloud_speed, \
         'shadows': args.shadows, \
         'video_widget': args.video_widget, \
         'wind_speed': args.wind_speed, \
         'update_rate': args.update_rate, \
         'realtime_factor': args.realtime_factor, \
         'ambient_light': args.ambient_light, \
         'background_light': args.background_light, \
         'use_spherical_coords': args.use_spherical_coords, \
         'latitude': deg_latitude, \
         'longitude': deg_lognitude, \
         'altitude': m_altitude, \
         'world_name': args.world_name, \
         'embedded_models': args.embedded_models, \
         'fog_params': args.fog_params, \
         'set_physics': args.set_physics, \
         'ode_threads': args.ode_threads}

        
    
    if (not os.path.isdir('/tmp/gazebo/worlds')):
        try: 
            os.makedirs('/tmp/gazebo/worlds', exist_ok = True) 
        except OSError as error: 
            print("Directory creation error.")

    result = template.render(d)
    if args.output_file:
        filename_out = args.output_file
    else:
        filename_out = '{:s}/{:s}.world'.format("/tmp/gazebo/worlds",args.world_name)

    with open(filename_out, 'w') as f_out:
        print(('{:s} -> {:s}'.format(default_filename, filename_out)))
        f_out.write(result)

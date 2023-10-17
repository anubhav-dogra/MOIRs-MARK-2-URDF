from xml.etree.ElementTree import Element, SubElement, Comment
import sys
import os

sys.path.append(os.path.abspath(os.getcwd()))
from ElementTree_pretty import prettify

# Using MACROS
class RobotURDF():
	def __init__(self):
		# Implement the side-opposite algorithm
		self.opp = 0		# self.opp == 0 implies construction along Z and self.opp == 1 implies construction along X
		self.robot = Element('robot')		# Make the first URDF Element
		self.name = input("Enter the name of the robot: ")		# Name of the robot
		self.robot.set('name', str(self.name))				# Set it in the urdf file
		self.robot.set('xmlns:xacro', "http://ros.org/wiki/xacro")
		
		self.type = input("Enter the type configuration: ")		# Set the Type Configuration
		
		include = SubElement(self.robot, 'xacro:include')
		include.set('filename', '$(find moir_mark2_urdf_ros)/urdf/modular_robot.urdf.xacro')	# Specify the MACRO File
		
		offset_length = float(input("Enter the initial offset length: "))		# Specify the initial length
		
		self.pedestal = SubElement(self.robot, "xacro:pedestal")		# Add the pedestal
		# Set the parameters of pedestal
		self.pedestal.set('length', str(offset_length))
		self.pedestal.set('xyz', "0 0 " + str(offset_length/2))
		self.pedestal.set('child', 'module_1')
		
		# A buffer to store the functions that are called
		# This allows us to change the configuration of previous joints (to allow z_twist)
		# After it is filled the generate_urdf function is called on this buffer
		# The format of buffer is:
		# [command, link_type, module_name, link_name, joint_name, child_name, trans_name, act_name, twist, z_twist, mass]
		self.buffer = []
		# For Pedestal
		self.buffer.append([None, None, None, None, None, None, None, None, None, 0, None])		# Only z_twist is of interest in our case

		# print prettify(robot)
		
	# Half without length module
	# module_name specifies the name of the module link
	# joint_name specifies the name of the module joint
	# child_name specifies the name of the next module link
	# twist is the twist to be given
	def half_without_length(self, module_name, joint_name, child_name, trans_name, act_name, twist=0, z_twist=0, mass=1):
		if(mass == 1):
			module = SubElement(self.robot, 'xacro:light-module')		# Call the macro: module
		else:
			module = SubElement(self.robot, 'xacro:heavy-module')
			
		module.set('name', module_name)				# Set the parameters
		
		# Set the parameters based on construction axis(refer to the diagrams for more details)
		if(self.opp == 0):
			module.set('xyz_module', "0 0 0.075")
			module.set('rpy_module', "0 -1.57 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "-0.02974 0 0.075")
			module.set('rpy_joint', "0 " + str(-1.57 + twist) + " 0")
		else:
			module.set('xyz_module', "0.075 0 0")
			module.set('rpy_module', "0 0 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "0.075 0 0.02974")
			module.set('rpy_joint', "0 " + str(twist) + " 0")
		
		# Finally add the final joint of the module and set it's parameters
		# based on axes of construction
		module_joint = SubElement(self.robot, 'xacro:module_joint')
		module_joint.set('axis', "0 0 1")
			
		module_joint.set('name', joint_name)
		module_joint.set('parent', module_name + "_link")
		module_joint.set('child', child_name)

		module_joint.set('xyz', "0 0 0.073")
		module_joint.set('rpy', "0 0 " + str(z_twist))
			
		transmission = SubElement(self.robot, 'xacro:transmission_tag')
		transmission.set('joint_name', joint_name)
		transmission.set('trans_name', trans_name)
		transmission.set('act_name', act_name)
		# Change direction of construction
		self.opp = 0

		
	# Full without length module
	# module_name specifies the name of the module link
	# joint_name specifies the name of the module joint
	# child_name specifies the name of the next module link
	# twist is the twist to be given
	def full_without_length(self, module_name, joint_name, child_name, trans_name, act_name, twist=0, z_twist=0, mass=1):
		if(mass == 1):
			module = SubElement(self.robot, 'xacro:light-module')		# Call the macro: module
		else:
			module = SubElement(self.robot, 'xacro:heavy-module')
			
		module.set('name', module_name)				# Set the parameters
		
		# Set the parameters based on construction axis(refer to the diagrams for more details)
		if(self.opp == 0):
			module.set('xyz_module', "0 0 0.045")
			module.set('rpy_module', "0 0 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "0 0 0.07474")
			module.set('rpy_joint', "0 " + str(twist) + " 0")
		else:
			module.set('xyz_module', "0.045 0 0")
			module.set('rpy_module', "0 1.57 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "0.07474 0 0")
			module.set('rpy_joint', "0 " + str(1.57 + twist) + " 0")

		# Finally add the final joint of the module and set it's parameters
		# based on axes of construction
		module_joint = SubElement(self.robot, 'xacro:module_joint')
		module_joint.set('axis', "0 0 1")
			
		module_joint.set('name', joint_name)
		module_joint.set('parent', module_name + "_link")
		module_joint.set('child', child_name)
		
		module_joint.set('xyz', "0 0 0.073")
		module_joint.set('rpy', "0 0 " + str(z_twist))
			
		transmission = SubElement(self.robot, 'xacro:transmission_tag')
		transmission.set('joint_name', joint_name)
		transmission.set('trans_name', trans_name)
		transmission.set('act_name', act_name)
		# Change direction of construction
		self.opp = 0
		
	# Half with length module
	# link_type specifies the type of passive link(0 or 1)
	# 0 is the one that does not change the construction
	# module_name specifies the name of the module link
	# link_name specifies the name of the pipe link
	# joint_name specifies the name of the module joint
	# child_name specifies the name of the next module link
	# length is the length of the pipe link
	# twist is the twist to be given
	def half_with_length(self, link_type, module_name, link_name, joint_name, child_name, trans_name, act_name, twist=0, z_twist=0, mass=1):
		if(mass == 1):
			module = SubElement(self.robot, 'xacro:light-module')		# Call the macro: module
		else:
			module = SubElement(self.robot, 'xacro:heavy-module')
			
		module.set('name', module_name)				# Set the parameters
		
		# Set the parameters based on construction axis(refer to the diagrams for more details)
		if(self.opp == 0):
			module.set('xyz_module', "0 0 0.075")
			module.set('rpy_module', "0 -1.57 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "-0.02974 0 0.075")
			module.set('rpy_joint', "0 " + str(-1.57 + twist) + " 0")
		else:
			module.set('xyz_module', "0.075 0 0")
			module.set('rpy_module', "0 0 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "0.075 0 0.02974")
			module.set('rpy_joint', "0 " + str(twist) + " 0")
		
		# Finally add the final joint of the module and set it's parameters
		# based on axes of construction
		module_joint = SubElement(self.robot, "xacro:module_joint")
		module_joint.set('axis', "0 0 1")
		
		module_joint.set('name', joint_name)
		module_joint.set('parent', module_name + "_link")
		module_joint.set('child', link_name)
		
		module_joint.set('xyz', "0 0 0.073")
		module_joint.set('rpy', "0 0 0")
			
		transmission = SubElement(self.robot, 'xacro:transmission_tag')
		transmission.set('joint_name', joint_name)
		transmission.set('trans_name', trans_name)
		transmission.set('act_name', act_name)
		
		# Now add the pipe link that is attached to our module motor
		# Set the parameters based on axes of construction
		if(link_type == 1):
			link = SubElement(self.robot, "xacro:pipe")
			link.set('name', link_name)

			link.set('rpy', "0 0 0")
			link.set('xyz', "0 0 0")
		
		else:
			link = SubElement(self.robot, "xacro:curved")
			link.set('name', link_name)
			if(self.opp == 0):
				link.set('rpy', "0 0 0")
				link.set('xyz', "0.0065 0 0")
			else:
				link.set('rpy', "0 0 0")
				link.set('xyz', "0 0 0.0065")
		
		# Add the final fixed joint of this module
		# Set the parameters based on axes of construction
		fixed_joint = SubElement(self.robot, "xacro:fixed")
		fixed_joint.set('name', "fixed_"+joint_name)
		fixed_joint.set('parent', link_name)
		fixed_joint.set('child', child_name)
		
		if(link_type == 1):
			# Link Type 1
			fixed_joint.set('xyz', "0.22 0 -0.015")
			fixed_joint.set('rpy', str(z_twist) + " 0 0")
			
		else:
			# Link Type 2
			fixed_joint.set('xyz', "0.115 0 -0.105")
			fixed_joint.set('rpy', str(z_twist) + " 0 0")
				
		# Change the direction of construction
		self.opp = 1
		
	# Full with length module
	# link_type specifies the type of passive_link(0 or 1)
	# 0 is the one that does not change the construction
	# module_name specifies the name of the module link
	# link_name specifies the name of the pipe link
	# joint_name specifies the name of the module joint
	# child_name specifies the name of the next module link
	# length is the length of the pipe link
	# twist is the twist to be given
	def full_with_length(self, link_type, module_name, link_name, joint_name, child_name, trans_name, act_name, twist=0, z_twist=0, mass=1):
		if(mass == 1):
			module = SubElement(self.robot, 'xacro:light-module')		# Call the macro: module
		else:
			module = SubElement(self.robot, 'xacro:heavy-module')
			
		module.set('name', module_name)				# Set the parameters
		
		# Set the parameters based on construction axis(refer to the diagrams for more details)
		if(self.opp == 0):
			module.set('xyz_module', "0 0 0.045")
			module.set('rpy_module', "0 0 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "0 0 0.07474")
			module.set('rpy_joint', "0 " + str(twist) + " 0")
		else:
			module.set('xyz_module', "0.045 0 0")
			module.set('rpy_module', "0 1.57 0")
			module.set('xyz_motor', "0 0 0")
			module.set('rpy_motor', "0 0 0")
			module.set('xyz_joint', "0.07474 0 0")
			module.set('rpy_joint', "0 " + str(1.57 + twist) + " 0")
		
		# Finally add the final joint of the module and set it's parameters
		# based on axes of construction
		module_joint = SubElement(self.robot, "xacro:module_joint")
		module_joint.set('axis', "0 0 1")
			
		module_joint.set('name', joint_name)
		module_joint.set('parent', module_name + "_link")
		module_joint.set('child', link_name)
		
		module_joint.set('xyz', "0 0 0.073")
		module_joint.set('rpy', "0 0 0")
			
		transmission = SubElement(self.robot, 'xacro:transmission_tag')
		transmission.set('joint_name', joint_name)
		transmission.set('trans_name', trans_name)
		transmission.set('act_name', act_name)
		
		# Now add the pipe link that is attached to our module motor
		# Set the parameters based on axes of construction
		if(link_type == 1):
			link = SubElement(self.robot, "xacro:pipe")
			link.set('name', link_name)
			
			link.set('rpy', "0 0 0")
			link.set('xyz', "0 0 0")
		
		else:
			link = SubElement(self.robot, "xacro:curved")
			link.set('name', link_name)
			
			link.set('rpy', "0 0 0")
			link.set('xyz', "0 0 0.0065")
		
		# Add the final fixed joint of this module
		# Set the parameters based on axes of construction
		fixed_joint = SubElement(self.robot, "xacro:fixed")
		fixed_joint.set('name', "fixed_"+joint_name)
		fixed_joint.set('parent', link_name)
		fixed_joint.set('child', child_name)
		
		if(link_type == 1):
			# Link Type 1 
			fixed_joint.set('xyz', "0.22 0 -0.015")
			fixed_joint.set('rpy', str(z_twist) + " 0 0")
			
		else:
			# Link Type 2 
			fixed_joint.set('xyz', "0.11 0 -0.10")
			fixed_joint.set('rpy', str(z_twist) + " 0 0")
				
		# Change the direction of construction
		self.opp = 1
		
	def fill_buffer(self):
		# From the xacro:macro file
		module_number = 1
		joint_number = 1
		link_number = 1
		trans_number = 1
		
		# Type configuration required as well!
		# buffer format: [command, link_type, module_name, link_name, joint_name, child_name, trans_name, act_name, twist, z_twist, mass]
		# if command is heavy then mass is 2, otherwise for any other input default mass of 1 will be taken, for now this works fine!
		
		number_of_modules = input("Enter the number of modules required: ")
		number_of_modules = int(number_of_modules)
		
		while(number_of_modules != 0):
			if(int(self.type) == 1):
				# The configuration type is 1. This implies that there is no twist to be provided. Hence we will only take 4 inputs from the user
				command = input('Enter module configuration: ').split(' ')
				heavy = int(command[0][0] == "h")
				module = int(command[0][1])
				
				# Append to buffer the appropriate values
				if(module < 3):
					self.buffer.append([module, None, "module_"+str(module_number), None, "joint_"+str(joint_number), "module_"+str(module_number+1), "transmission_"+str(trans_number), "motor_"+str(trans_number), 0, 0, 1+heavy])
					module_number += 1; joint_number += 1; trans_number += 1
				else:
					# Take as raw input for curved or pipe!!
					link_type = int(command[1])
					self.buffer.append([module, link_type, "module_"+str(module_number), "link_"+str(link_number), "joint_"+str(joint_number), "module_"+str(module_number + 1), "transmission_"+str(trans_number), "motor_"+str(trans_number), 0, 0, 1+heavy])
					module_number += 1; link_number += 1; joint_number += 1; trans_number += 1
					
			elif(int(self.type) == 2):
				# The configuration type is 2. This implies that there is a twist in Z axis. We take 5 inputs from the user
				command = input('Enter module configuration: ').split(' ')
				heavy = int(command[0][0] == "h")
				module = int(command[0][1])
				z_twist = float(command[1])
				index_to_change = len(self.buffer) - 1
				
				# Append to buffer the appropriate values
				if(module < 3):
					self.buffer.append([module, None, "module_"+str(module_number), None, "joint_"+str(joint_number), "module_"+str(module_number+1), "transmission_"+str(trans_number), "motor_"+str(trans_number), 0, 0, 1+heavy])
					module_number += 1; joint_number += 1; trans_number += 1
					self.buffer[index_to_change][9] = z_twist	# Change the z twist of the final joint of previous module
				else:
					link_type = int(command[2])
					self.buffer.append([module, link_type, "module_"+str(module_number), "link_"+str(link_number), "joint_"+str(joint_number), "module_"+str(module_number + 1), "transmission_"+str(trans_number), "motor_"+str(trans_number), 0, 0, 1+heavy])
					module_number += 1; link_number += 1; joint_number += 1; trans_number += 1
					self.buffer[index_to_change][9] = z_twist	# Change the z twist of the final joint of previous module
				
			elif(int(self.type) == 3):
				# The configuration type is 3. This implies that there is twist in Y axis. We take 5 inputs from the user
				command = input('Enter module configuration: ').split(' ')
				heavy = int(command[0][0] == "h")
				module = int(command[0][1])
				twist = float(command[1])
				# No index to change, only current modules affected
				
				# Append to buffer the appropriate values
				if(module < 3):
					self.buffer.append([module, None, "module_"+str(module_number), None, "joint_"+str(joint_number), "module_"+str(module_number+1), "transmission_"+str(trans_number), "motor_"+str(trans_number), twist, 0, 1+heavy])
					module_number += 1; joint_number += 1; trans_number += 1
				else:
					link_type = int(command[2])
					self.buffer.append([module, link_type, "module_"+str(module_number), "link_"+str(link_number), "joint_"+str(joint_number), "module_"+str(module_number + 1), "transmission_"+str(trans_number), "motor_"+str(trans_number), twist, 0, 1+heavy])
					module_number += 1; link_number += 1; joint_number += 1; trans_number += 1

			elif(int(self.type) == 4):
				# The configuration type is 4. This implies that there is a twist in Z axis and Y axis. We take 6 inputs from the user
				command = input('Enter module configuration: ').split(' ')
				heavy = int(command[0][0] == "h")
				module = int(command[0][1])
				z_twist = float(command[1])
				twist = float(command[2])
				index_to_change = len(self.buffer) - 1
				
				# Append to buffer the appropriate values
				if(module < 3):
					self.buffer.append([module, None, "module_"+str(module_number), None, "joint_"+str(joint_number), "module_"+str(module_number+1), "transmission_"+str(trans_number), "motor_"+str(trans_number), twist, 0, 1+heavy])
					module_number += 1; joint_number += 1; trans_number += 1
					self.buffer[index_to_change][9] = z_twist	# Change the z twist of the final joint of previous module
				else:
					link_type = int(command[3])
					self.buffer.append([module, link_type, "module_"+str(module_number), "link_"+str(link_number), "joint_"+str(joint_number), "module_"+str(module_number + 1), "transmission_"+str(trans_number), "motor_"+str(trans_number), twist, 0, 1+heavy])
					module_number += 1; link_number += 1; joint_number += 1; trans_number += 1
					self.buffer[index_to_change][9] = z_twist	# Change the z twist of the final joint of previous module					


			number_of_modules -= 1
			
		self.joint_count = joint_number
			
		#self.buffer.append([None, "module"+str(module_number), None, None, None, None, None, None])		# Only module name is of use in final link
		
	
	def generate_urdf(self):
		# buffer format: [command, link_type, module_name, link_name, joint_name, child_name, trans_name, act_name, twist, z_twist, mass]
	
		# After filling the buffer call generate_urdf to generate the urdf file by going over the buffer matrix
		for module in self.buffer:
			if(module[0] == None):
				self.pedestal.set('rpy', "0 0 " + str(module[9]))
				continue
				
			# Used to decide the length of the module
			# Check whether length is zero or not!
			if(module[0] < 3):
				if(module[0] == 2):
					self.half_without_length(module[2], module[4], module[5], module[6], module[7], module[8], module[9], module[10])
				elif(module[0] == 1):
					self.full_without_length(module[2], module[4], module[5], module[6], module[7], module[8], module[9], module[10])
					
			else:
				if(module[0] == 4):
					self.half_with_length(module[1], module[2], module[3], module[4], module[5], module[6], module[7], module[8], module[9], module[10])
				elif(module[0] == 3):
					self.full_with_length(module[1], module[2], module[3], module[4], module[5], module[6], module[7], module[8], module[9], module[10])
					
		end_link = SubElement(self.robot, "link")
		end_link.set('name', 'module_'+str(len(self.buffer)))
		
		# Add gazebo tag
		gazebo = SubElement(self.robot, "gazebo")
		
		# Add control plugin
		control_plugin = SubElement(gazebo, "plugin")
		control_plugin.set('name', 'control')
		control_plugin.set('filename', "libgazebo_ros_control.so")
		
		# Add robot state publisher plugin
		state_plugin = SubElement(gazebo, "plugin")
		state_plugin.set('name', 'joint_state_publisher')
		state_plugin.set('filename', "libgazebo_ros_joint_state_publisher.so")
		joint_names = SubElement(state_plugin, "jointName")
		joint_string = ""
		for index in range(1, self.joint_count-1):
			joint_string += "joint_" + str(index) + ", "
		joint_string += "joint_" + str(self.joint_count-1)
		joint_names.text = joint_string
		
		
	def print_urdf(self):
		# Save the URDF File to appropriate location
		with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'urdf/generated/' + self.name + '.xacro'), 'w') as _file:
			_file.write(prettify(self.robot))
	
		# Print to terminal for debugging purposes
		print(prettify(self.robot))
		
		
# Call all the parameters
Example = RobotURDF()
Example.fill_buffer()
Example.generate_urdf()
Example.print_urdf()


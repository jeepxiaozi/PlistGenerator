#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright 2015 EricTang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#   Author  :   EricTang
#   E-mail  :   jeepxiaozi66@gmail.com
#   Date    :   2015/03/20 01:36:32
#   Desc    :	根据ipa生成plist文件，适用于iOS应用的企业级分发
#	Usage	:	将该文件放在与要处理的ipa文件同级目录下，cd到该目录，执行
# 				"""
# 				python3 PlistGenerator.py 
#				--ipaFileName=要处理的ipa文件名，无需.ipa格式结尾 
#				--appTitle=应用标题
#				--downloadUrl=实际放置.ipa文件的远程地址
#	Exanple	:	python3 PlistGenerator.py --ipaFileName=EricProject --appTitle=EricTang --downloadUrl=http://xxx.com/download/xxx.ipa

import zipfile
import plistlib
import re
import os
import sys
import getopt

# 当前路径
current_dir = os.getcwd() + "/"

def getPlistRoot(ipa_file_name):
	"""
	获取Plist文件内容
	"""
	file_path = current_dir + ipa_file_name + ".ipa"
	print(file_path)
	if os.path.exists(file_path):
		ipa_file = zipfile.ZipFile(file_path)
		info_plist = getPlistFromZipFile(ipa_file)
		info_plist_data = ipa_file.read(info_plist)
		info_plist_root = plistlib.loads(info_plist_data)
		return info_plist_root
# end def

def getPlistFromZipFile(zip_file):
	"""
	找到Info.plist文件地址
	"""
	file_name_list = zip_file.namelist()
	info_plist_re_pattern = re.compile(r"Payload/[^/]*.app/Info.plist")
	for file_name in file_name_list:
		match = info_plist_re_pattern.match(file_name)
		if match is not None:
			print(u"bingo，找到文件" + file_name)
			return match.group()
# end def

def generatePlist(info_plist_root, app_title, ipd_url):
	"""
	根据读取到的Info.plist文件内容生成plist文件
	"""
	print(u"应用名 : %s" % info_plist_root["CFBundleDisplayName"])
	print(u"Bundle Id : %s" % info_plist_root["CFBundleIdentifier"])
	print(u"版本号 : %s" % info_plist_root["CFBundleShortVersionString"])
	print(u"应用标题 : %s" % app_title)
	print(u"ipa文件下载地址 : %s" % ipd_url)
	# 组装要生成的plist文件
	metadata_dict = {
		"bundle-identifier" : info_plist_root["CFBundleIdentifier"],
		"bundle-version" : info_plist_root["CFBundleShortVersionString"],
		"kind" : "software",
		"title" : app_title,
	}
	pl = dict (
		items = [
			dict(
				assets = [dict(kind = "software-package", url = ipd_url)],
				metadata = metadata_dict,
				)
		],
		)
	with open(info_plist_root["CFBundleDisplayName"] + ".plist", "wb") as fp:
		plistlib.dump(pl, fp)
# end def

if __name__ == "__main__":
	shortargs = 'h:'
	longargs = ['ipaFileName=', 'appTitle=', 'downloadUrl=']
	opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
	ipa_file_name_arg = ""
	app_title_arg = ""
	ipa_url_arg = ""
	for arg, val in opts:
		if arg == "--ipaFileName":
			ipa_file_name_arg = val
		elif arg == "--appTitle":
			app_title_arg = val
		elif arg == "--downloadUrl":
			ipa_url_arg = val

	generatePlist(getPlistRoot(ipa_file_name_arg), app_title_arg, ipa_url_arg)
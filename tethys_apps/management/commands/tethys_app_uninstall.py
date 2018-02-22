"""
********************************************************************************
* Name: collectworkspaces.py
* Author: Nathan Swain
* Created On: August 6, 2015
* Copyright: (c) Brigham Young University 2015
* License: BSD 2-Clause
********************************************************************************
"""
import os
import shutil
import site
import subprocess

from django.core.management.base import BaseCommand
from tethys_apps.helpers import get_installed_tethys_apps, get_installed_tethys_extensions


class Command(BaseCommand):
    """
    Command class that handles the uninstall command for uninstall Tethys apps.
    """
    def add_arguments(self, parser):
        parser.add_argument('app_or_extension', nargs='+', type=str)
        parser.add_argument('-e', '--extension', dest='is_extension', default=False, action='store_true')

    def handle(self, *args, **options):
        """
        Remove the app from disk and in the database
        """
        app_or_extension = "App" if not options['is_extension'] else 'Extension'
        PREFIX = 'tethysapp' if not options['is_extension'] else 'tethysext'
        item_name = options['app_or_extension'][0]
        installed_items = get_installed_tethys_apps()
        installed_items.update(get_installed_tethys_extensions())

        if PREFIX in item_name:
            prefix_length = len(PREFIX) + 1
            item_name = item_name[prefix_length:]

        if item_name not in installed_items:
            self.stdout.write('WARNING: {} with name "{}" cannot be uninstalled, because it is not installed.'.format(app_or_extension, item_name))
            exit(0)

        item_with_prefix = '{0}-{1}'.format(PREFIX, item_name)

        # Confirm
        valid_inputs = ('y', 'n', 'yes', 'no')
        no_inputs = ('n', 'no')

        overwrite_input = raw_input('Are you sure you want to uninstall "{0}"? (y/n): '.format(item_with_prefix)).lower()

        while overwrite_input not in valid_inputs:
            overwrite_input = raw_input('Invalid option. Are you sure you want to '
                                        'uninstall "{0}"? (y/n): '.format(item_with_prefix)).lower()

        if overwrite_input in no_inputs:
            self.stdout.write('Uninstall cancelled by user.')
            exit(0)

        # Remove app from database
        from tethys_apps.models import TethysApp, TethysExtension
        TethysModel = TethysApp if not options['is_extension'] else TethysExtension
        db_app = TethysModel.objects.get(package=item_name)
        db_app.delete()

        if not options['is_extension']:
            try:
                # Remove directory
                shutil.rmtree(installed_items[item_name])
            except OSError:
                # Remove symbolic link
                os.remove(installed_items[item_name])

        # Uninstall using pip
        process = ['pip', 'uninstall', '-y', '{0}-{1}'.format(PREFIX, item_name)]

        try:
            subprocess.Popen(process, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
        except KeyboardInterrupt:
            pass

        for site_package in site.getsitepackages():
            try:
                os.remove(os.path.join(site_package, "{}-{}-nspkg.pth".format(PREFIX, item_name)))
            except:
                continue

        self.stdout.write('{} "{}" successfully uninstalled.'.format(app_or_extension, item_with_prefix))

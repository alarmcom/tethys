# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tethys_compute.utilities


class Migration(migrations.Migration):

    initial = True

    replaces = [(b'tethys_compute', '0001_initial'), (b'tethys_compute', '0002_initialize_settings'),
                (b'tethys_compute', '0003_auto_20150529_1651'), (b'tethys_compute', '0004_auto_20150812_1915'),
                (b'tethys_compute', '0005_auto_20150914_1712'), (b'tethys_compute', '0006_auto_20151221_2207'),
                (b'tethys_compute', '0006_auto_20151026_2142'), (b'tethys_compute', '0007_merge'),
                (b'tethys_compute', '0008_start_condorjob_refactor'),
                (b'tethys_compute', '0009_condorjob_data_migration'),
                (b'tethys_compute', '0010_finish_condorjob_refactor'), (b'tethys_compute', '0011_delete_cluster'),
                (b'tethys_compute', '0012_delete_settings')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CondorPyJob',
            fields=[
                ('condorpyjob_id', models.AutoField(primary_key=True, serialize=False)),
                ('_attributes', tethys_compute.utilities.DictionaryField(default=b'')),
                ('_num_jobs', models.IntegerField(default=1)),
                ('_remote_input_files', tethys_compute.utilities.ListField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='CondorPyWorkflow',
            fields=[
                ('condorpyworkflow_id', models.AutoField(primary_key=True, serialize=False)),
                ('_max_jobs', tethys_compute.utilities.DictionaryField(blank=True, default=b'')),
                ('_config', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CondorWorkflowNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('pre_script', models.CharField(blank=True, max_length=1024, null=True)),
                ('pre_script_args', models.CharField(blank=True, max_length=1024, null=True)),
                ('post_script', models.CharField(blank=True, max_length=1024, null=True)),
                ('post_script_args', models.CharField(blank=True, max_length=1024, null=True)),
                ('variables', tethys_compute.utilities.DictionaryField(blank=True, default=b'')),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=128, null=True)),
                ('retry', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('retry_unless_exit_value', models.IntegerField(blank=True, null=True)),
                ('pre_skip', models.IntegerField(blank=True, null=True)),
                ('abort_dag_on', models.IntegerField(blank=True, null=True)),
                ('abort_dag_on_return_value', models.IntegerField(blank=True, null=True)),
                ('dir', models.CharField(blank=True, max_length=1024, null=True)),
                ('noop', models.BooleanField(default=False)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('host', models.CharField(max_length=1024)),
                ('username', models.CharField(blank=True, max_length=1024, null=True)),
                ('password', models.CharField(blank=True, max_length=1024, null=True)),
                ('private_key_path', models.CharField(blank=True, max_length=1024, null=True)),
                ('private_key_pass', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TethysJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('description', models.CharField(blank=True, default=b'', max_length=2048)),
                ('label', models.CharField(max_length=1024)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('execute_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('completion_time', models.DateTimeField(blank=True, null=True)),
                ('workspace', models.CharField(default=b'', max_length=1024)),
                ('extended_properties', tethys_compute.utilities.DictionaryField(blank=True, default=b'')),
                ('_process_results_function', models.CharField(blank=True, max_length=1024, null=True)),
                ('_status', models.CharField(choices=[(b'PEN', b'Pending'), (b'SUB', b'Submitted'), (b'RUN', b'Running'), (b'COM', b'Complete'), (b'ERR', b'Error'), (b'ABT', b'Aborted'), (b'VAR', b'Various'), (b'VCP', b'Various-Complete')], default=b'PEN', max_length=3)),
            ],
            options={
                'verbose_name': 'Job',
            },
        ),
        migrations.CreateModel(
            name='BasicJob',
            fields=[
                ('tethysjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tethys_compute.TethysJob')),
            ],
            bases=('tethys_compute.tethysjob',),
        ),
        migrations.CreateModel(
            name='CondorBase',
            fields=[
                ('tethysjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tethys_compute.TethysJob')),
                ('cluster_id', models.IntegerField(blank=True, default=0)),
                ('remote_id', models.CharField(blank=True, max_length=32, null=True)),
            ],
            bases=('tethys_compute.tethysjob',),
        ),
        migrations.CreateModel(
            name='CondorWorkflowJobNode',
            fields=[
                ('condorpyjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tethys_compute.CondorPyJob')),
                ('condorworkflownode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tethys_compute.CondorWorkflowNode')),
            ],
            bases=('tethys_compute.condorworkflownode', 'tethys_compute.condorpyjob'),
        ),
        migrations.AddField(
            model_name='tethysjob',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='condorworkflownode',
            name='parent_nodes',
            field=models.ManyToManyField(related_name='children_nodes', to='tethys_compute.CondorWorkflowNode'),
        ),
        migrations.AddField(
            model_name='condorworkflownode',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='node_set', to='tethys_compute.CondorPyWorkflow'),
        ),
        migrations.CreateModel(
            name='CondorJob',
            fields=[
                ('condorpyjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tethys_compute.CondorPyJob')),
                ('condorbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tethys_compute.CondorBase')),
            ],
            bases=('tethys_compute.condorbase', 'tethys_compute.condorpyjob'),
        ),
        migrations.CreateModel(
            name='CondorWorkflow',
            fields=[
                ('condorpyworkflow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tethys_compute.CondorPyWorkflow')),
                ('condorbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tethys_compute.CondorBase')),
            ],
            bases=('tethys_compute.condorbase', 'tethys_compute.condorpyworkflow'),
        ),
        migrations.AddField(
            model_name='condorbase',
            name='scheduler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tethys_compute.Scheduler'),
        ),
    ]
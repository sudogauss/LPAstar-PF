SHELL := /bin/bash

VENV = lpastar_venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

VERSION=0.0.1
PACKAGE=lpastar_pf
ARTIFACT="$(PACKAGE)/dist/$(PACKAGE)-$(VERSION)-py3-none-any.whl"

ROS_DISTRO=foxy
ROS_PATH_TO_CONFIG=ros/ros2_ws/src/config/pf_default_config.yaml
ROS=ros2
ROS_BUILD=colcon
ROSDEP=rosdep

CUR=$(PWD)


.PHONY: init test build install clean ros_interfaces ros_node \
		ros_docker ros_run ros_run_docker ros_node_only ros_run_only

# lpastar_pf package targets
$(VENV)/bin/activate: requirements.txt
	if [ ! -d "./lpastar_venv" ]; then python3 -m venv lpastar_venv; fi
	$(PIP) install -r requirements.txt

init: requirements.txt
	if [ ! -d "./lpastar_venv" ]; then python3 -m venv lpastar_venv; fi
	$(PIP) install -r requirements.txt

test: $(VENV)/bin/activate
	pytest lpastar_pf

$(ARTIFACT): $(VENV)/bin/activate test
	$(PYTHON) -m build $(PACKAGE)

build: $(VENV)/bin/activate test
	$(PYTHON) -m build $(PACKAGE)

install: $(ARTIFACT)
	$(PIP) install $(ARTIFACT)

clean:
	rm -rf $(PACKAGE)/dist
	rm -rf .pytest_cache
	rm -rf __pycache__

# ros targets

ros_interfaces:
	cd ros/ros2_ws; $(ROSDEP) install -i --from-path src --rosdistro $(ROS_DISTRO) -y; \
	$(ROS_BUILD) build --packages-select pf_interfaces; source install/setup.bash; cd $(CUR)

ros_node: install ros_interfaces
	cd ros/ros2_ws; echo $(PWD); $(ROSDEP) install -i --from-path src --rosdistro $(ROS_DISTRO) -y; \
	$(ROS_BUILD) build --packages-select ros_lpastar_pf; source install/setup.bash; cd $(CUR)

ros_node_only: ros_interfaces
	cd ros/ros2_ws; echo $(PWD); $(ROSDEP) install -i --from-path src --rosdistro $(ROS_DISTRO) -y; \
	$(ROS_BUILD) build --packages-select ros_lpastar_pf; source install/setup.bash; cd $(CUR)

ros_docker:
	echo "docker TODO"

ros_run: ros_node
	export PYTHONPATH=$(PWD)/lpastar_venv/lib/python3.8/site-packages:$(PYTHONPATH); \
	$(ROS) run ros_lpastar_pf ros_lpastar_pf $(ROS_PATH_TO_CONFIG)

ros_run_docker: ros_docker
	echo "ros run docker TODO"



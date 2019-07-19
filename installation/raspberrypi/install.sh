#!/usr/bin/env bash

set -e

APPS_DIR="/var/apps"
ENVS_DIR="/var/envs"
GIT_REPO="https://github.com/benjohnsonnlp/robosquirt.git"
APP_DIR="${APPS_DIR}/robosquirt"
ENV_DIR="${ENVS_DIR}/robosquirt"
ROBOSQUIRT_SERVICE_FILE="/lib/systemd/system/robosquirt.service"
MOISTMASTER_SERVICE_FILE="/lib/systemd/system/moistmaster.service"
SYSLOG_FILE="/etc/rsyslog.d/robosquirt.conf"
ROBOSQUIRT_LOG="/var/log/robosquirt.log"

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root or with sudo."
   exit 1
fi


# Create apps directory.
if [ ! -d "$APPS_DIR" ]; then
  mkdir -p $APPS_DIR
  chown pi:pi $APPS_DIR
  chmod 775 $APPS_DIR
  echo "Created apps directory: ${APPS_DIR}."
else
    echo "Apps directory (${APPS_DIR}) already exists. Skipping."
fi

# Create envs directory.
if [ ! -d "$ENVS_DIR" ]; then
  mkdir -p $ENVS_DIR
  chown pi:pi $ENVS_DIR
  chmod 775 $ENVS_DIR
  echo "Created virtual envs directory: ${ENVS_DIR}."
else
    echo "Virtual envs directory (${ENVS_DIR}) already exists. Skipping."
fi


# Clone project.
if [ ! -d "$APP_DIR" ]; then
  git clone $GIT_REPO $APP_DIR
  echo "Cloned project in: ${APP_DIR}."

else
    echo "Project already exists (${APP_DIR}). No need to clone from GitHub."
    cd $APP_DIR && git pull
fi

# Make virtualenv and install requirements.
if [ ! -d "$ENV_DIR" ]; then
  virtualenv $ENV_DIR --python=`which python3`
  source "${ENV_DIR}/bin/activate"
  pip install -r "${APP_DIR}/requirements/dev.txt"
  echo "Project requirements installed.."
else
    echo "Project virtualenv already exists (${ENV_DIR}). No need to install requirements."
fi

# Install systemd service: robosquirt.
if [ ! -f "$ROBOSQUIRT_SERVICE_FILE" ]; then
  cp robosquirt.service $ROBOSQUIRT_SERVICE_FILE

  echo "Copied systemd service definition: ${ROBOSQUIRT_SERVICE_FILE}."
else
    echo "Systemd service file already exists (${ROBOSQUIRT_SERVICE_FILE}). Skipping."
fi

# Install systemd service: moistmaster.
if [ ! -f "$MOISTMASTER_SERVICE_FILE" ]; then
  cp moistmaster.service $MOISTMASTER_SERVICE_FILE

  echo "Copied systemd service definition: ${MOISTMASTER_SERVICE_FILE}."
else
    echo "Systemd service file already exists (${MOISTMASTER_SERVICE_FILE}). Skipping."
fi


# Install rsyslog config.
if [ ! -f "$SYSLOG_FILE" ]; then
  cp robosquirt.conf $SYSLOG_FILE
  echo "Copied rsyslog config: ${SYSLOG_FILE}."
  declare -a StringArray=("/var/log/robosquirt.log" "/var/log/moistmaster.log")
  for log in "${StringArray[@]}"
  do
    touch $log
    chown root:adm $log
    chmod 664 $log
    echo "Initialized log file: ${log}."
  done
  sudo systemctl restart rsyslog
else
    echo "Rsyslog already configured (${SYSLOG_FILE}). Skipping."
fi






echo "All done!"

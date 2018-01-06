#!/bin/sh

SCRIPT_PATH=`dirname $0`
cd $SCRIPT_PATH

for f in ./*; do
  if [ -d "$f" ]; then
    VERSION=`cat $f/addon.xml | grep "addon id" | awk '{match($0,"version=\"(.*?)\" ",a)}END{print a[1]}'`
    ADDON_NAME=`basename $f`
    echo "Plugin found: $ADDON_NAME/$ADDON_NAME-$VERSION"
    rm -f "$ADDON_NAME/$ADDON_NAME-$VERSION.zip"
    zip -r "$ADDON_NAME/$ADDON_NAME-$VERSION.zip" "$ADDON_NAME" -x "*.zip*"
  fi
done

python addons_xml_generator.py

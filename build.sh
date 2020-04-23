#!/bin/bash


buildFolder="FlowState"
dllDestination="$buildFolder"
gameDestination="$buildFolder"
textureDestination="$buildFolder/textures"
sounds="$buildFolder/sounds"
scripts="$buildFolder/scripts"
maps="$buildFolder/maps"
ghosts="$buildFolder/ghosts"
fonts="$buildFolder/fonts"
python="$buildFolder/2.79"

#windows files
dllFiles=( "api-ms-win-core-console-l1-1-0.dll" "api-ms-win-core-datetime-l1-1-0.dll" "api-ms-win-core-debug-l1-1-0.dll" "api-ms-win-core-errorhandling-l1-1-0.dll" "api-ms-win-core-file-l1-1-0.dll" "api-ms-win-core-file-l1-2-0.dll" "api-ms-win-core-file-l2-1-0.dll" "api-ms-win-core-handle-l1-1-0.dll" "api-ms-win-core-heap-l1-1-0.dll" "api-ms-win-core-interlocked-l1-1-0.dll" "api-ms-win-core-libraryloader-l1-1-0.dll" "api-ms-win-core-localization-l1-2-0.dll" "api-ms-win-core-memory-l1-1-0.dll" "api-ms-win-core-namedpipe-l1-1-0.dll" "api-ms-win-core-processenvironment-l1-1-0.dll" "api-ms-win-core-processthreads-l1-1-0.dll" "api-ms-win-core-processthreads-l1-1-1.dll" "api-ms-win-core-profile-l1-1-0.dll" "api-ms-win-core-rtlsupport-l1-1-0.dll" "api-ms-win-core-string-l1-1-0.dll" "api-ms-win-core-synch-l1-1-0.dll" "api-ms-win-core-synch-l1-2-0.dll" "api-ms-win-core-timezone-l1-1-0.dll" "api-ms-win-core-sysinfo-l1-1-0.dll" "api-ms-win-core-util-l1-1-0.dll" "api-ms-win-crt-conio-l1-1-0.dll" "api-ms-win-crt-convert-l1-1-0.dll" "api-ms-win-crt-environment-l1-1-0.dll" "api-ms-win-crt-filesystem-l1-1-0.dll" "api-ms-win-crt-heap-l1-1-0.dll" "api-ms-win-crt-locale-l1-1-0.dll" "api-ms-win-crt-math-l1-1-0.dll" "api-ms-win-crt-multibyte-l1-1-0.dll" "api-ms-win-crt-private-l1-1-0.dll" "api-ms-win-crt-process-l1-1-0.dll" "api-ms-win-crt-runtime-l1-1-0.dll" "api-ms-win-crt-stdio-l1-1-0.dll" "api-ms-win-crt-string-l1-1-0.dll" "api-ms-win-crt-time-l1-1-0.dll" "api-ms-win-crt-utility-l1-1-0.dll" "avcodec-58.dll" "avdevice-58.dll" "avformat-58.dll" "avutil-56.dll" "BlendThumb64.dll" "concrt140.dll" "libsndfile-1.dll" "msvcp140.dll" "OpenAL32.dll" "pthreadVC2.dll" "python37.dll" "SDL2.dll" "swresample-3.dll" "swscale-5.dll" "ucrtbase.dll" "vcomp140.dll" "vcruntime140.dll" )
blends=( "userInterfaces.blend" "assets.blend" "actors.blend" )
game="game.exe"

#mac files
mac="game.blend"
blenderplayer="blenderplayer"

#put it all together
#delete existing build folder
rm -rf $buildFolder
echo "deleted $buildFolder"
mkdir $buildFolder
echo "created $buildFolder"

echo "copying game file"
cp $game $gameDestination

echo "copying textures..."
cp -r textures $gameDestination
echo "copying sounds..."
cp -r sounds $gameDestination
echo "copying scripts..."
cp -r scripts $gameDestination
echo "copying maps..."
cp -r maps $gameDestination
echo "copying ghosts..."
cp -r ghosts $gameDestination
echo "copying fonts..."
cp -r fonts $gameDestination
echo "copying 2.79..."
cp -r "2.79" $gameDestination

#copy all the DLL file
for i in "${dllFiles[@]}"
do
   echo "copying $i to $dllDestination"
   cp $i $dllDestination
done

for i in "${blends[@]}"
do
   echo "copying $i to $gameDestination"
   cp $i $gameDestination
done
rm -rf FlowState.zip
zip -r FlowState.zip FlowState

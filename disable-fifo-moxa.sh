#!/usr/bin/env bash

CMD=/usr/bin/setserial
ttys=$(ls /dev/ttyM*)

for i in $ttys; do
	/usr/bin/setserial ${i} uart 16450 > /dev/null 2>&1 || continue
done

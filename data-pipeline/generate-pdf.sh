#!/bin/bash

pandoc architecture.md \
    --toc --toc-depth 2 \
    -o architecture.pdf  
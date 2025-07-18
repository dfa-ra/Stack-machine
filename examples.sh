#!/bin/bash

LOG_FLAG=""

if [ "$1" == "-l" ]; then
    LOG_FLAG="-l"
    shift
fi

if [ -z "$1" ]; then
    echo "Usage: $0 [-l] <example_name>"
    echo "Available examples: hello, cat, hello_user_name, sort, prob2, ssm, vsm"
    exit 1
fi

case "$1" in
    "hello_user_name")
        YAML="example/hello_user_name/hello_user_name.yaml"
        FORTH="example/hello_user_name/hello_user_name.forth"
        ;;
    "cat")
        YAML="example/cat/cat.yaml"
        FORTH="example/cat/cat.forth"
        ;;
    "sort")
        YAML="example/sort/sort.yaml"
        FORTH="example/sort/sort.forth"
        ;;
    "arrays")
        YAML="example/arrays/arrays.yaml"
        FORTH="example/arrays/arrays.forth"
        ;;
    "ssm")
        YAML="example/vector_vs_scalar/scalar_sum_mas/ssm.yaml"
        FORTH="example/vector_vs_scalar/scalar_sum_mas/ssm.forth"
        ;;
    "vsm")
        YAML="example/vector_vs_scalar/vector_sum_mas/vsm.yaml"
        FORTH="example/vector_vs_scalar/vector_sum_mas/vsm.forth"
        ;;
    *)
        echo "Unknown example: $1"
        echo "Available examples: hello_user_name, sort, ssm, vsm"
        exit 1
        ;;
esac

if [ ! -f "$YAML" ]; then
    echo "Error: YAML file not found: $YAML"
    exit 1
fi

if [ ! -f "$FORTH" ]; then
    echo "Error: Forth file not found: $FORTH"
    exit 1
fi

if [ -n "$LOG_FLAG" ]; then
    python3 -m src.main -c "$YAML" -f "$FORTH" -l
else
    python3 -m src.main -c "$YAML" -f "$FORTH"
fi
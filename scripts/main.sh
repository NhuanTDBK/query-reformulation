echo "Running wrk with 1 thread and 1 connection for 60 seconds for short queries"
url='http://50.18.255.74:8040/rewrite'
wrk -t1 -c1 -d60s --latency -s short_query.lua "$url"

echo "Running wrk with 1 thread and 1 connection for 60 seconds for long queries"
wrk -t1 -c1 -d60s --latency -s long_query.lua "$url"

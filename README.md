Utility to parse the ring of cassandra for vnodes from `nodetool ring`

TODO:
- Currently only work with one DC, requires to split the nodetool ring per DC
- Multiple functions are currently enabled for calc but do not show results
Challenge is to understand how RF comes at play on "ownership" of each node in `nodetool status`
For now, this is disabled and the tool calculate raw ownership (before RF)
- Need to add filename as an argument
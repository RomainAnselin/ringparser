Utility to parse the ring of cassandra for vnodes from `nodetool ring` to check imbalance related to vnodes distribution

TODO:
- Currently only work with one DC, requires to split the nodetool ring per DC.
ie: to get ring info between DC1 and DC2
`sed -z -E 's/.*(DC1.*DC2).*/\1/p' nodetool/ring | tee nodetool/dcring`
- Multiple functions are currently enabled for calc but do not show results
Challenge is to understand how RF comes at play on "ownership" of each node in `nodetool status`
For now, this is disabled and the tool calculate raw ownership (before RF)

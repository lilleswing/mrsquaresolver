# mrsquaresolver
Mr Square Solver

This solves Mr. Square Levels using a depth first search.

https://play.google.com/store/apps/details?id=com.ludicside.mrsquare&hl=en


## Level Legend
| Tables        | Are           |
| ------------- |:-------------|
| s | Mr Square         |
| c | Confused Mr Square|
| f | Full              |
| e | Empty             |
| d | Down Arrow        |
| u | Up Arrow          | 
| l | Left Arrow        |
| r | Right Arrow       |
| w | Warp              |
| H | North-South Bridge|
| Z | East-West Bridge  |
| m | Magnet (not implemented) |

## TODO
Magnets

There are some inaccuracies with how the squares travel on arrow pads and warps.
I'm not sure if I should take an additional move step when on them.  This
generally doesn't come into play, except on the levels whitelisted in the tests.


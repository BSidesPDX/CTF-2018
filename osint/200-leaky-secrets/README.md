## Problem Statement
We're looking for a foothold into Future Gadget Labs network and thought their developers might have leaked some passwords somewhere. Do you know where to look to git some secrets?

## Solution
The Future Gadget Labs [https://futuregadgetlabs.org/](website) lists some employee names and gives you a rough idea of what those employees do. Using that information, one might reasonably suspect that their software developer has a github account. You can search for the developer (Jopher Jimzen) or the organization (futuregadgetlabs) and find a repository. He isn't super active but you should notice that one of his recent commits was "Removing secrets", so if you look at the diff for that commit you will find the flag.


## Flag
BsidesPDX{g1t_y0u_s0m3_s3cr3ts}
// BSidesPDX CTF 2018
// RE-100 Solution

package main

import (
        "fmt"
)

func goxor() {
    var solution string = ""
    challenge := []byte{61,44,22,27,26,12,47,59,39,4,24,79,15,23,76,13,32,13,10,19,76,74,32,11,76,23,32,8,79,13,78,27,32,79,7,72,25,2,117}

    for _, char := range challenge {
        charx := char ^ 0x7f
        solution += string(charx)
    }

    fmt.Println(solution + " is the correct flag!")
}

func main() {

    goxor()
}

// BSidesPDX CTF 2018
// RE-100

package main

import (
        "os"
        "fmt"
)

func goxor(input string) {
    //BSidesPDX{g0ph3r_rul35_t3h_w0r1d_0x7f} with each byte ^ by 0x7f
    challenge := []byte{61,44,22,27,26,12,47,59,39,4,24,79,15,23,76,13,32,13,10,19,76,74,32,11,76,23,32,8,79,13,78,27,32,79,7,72,25,2,117}
    x := 0

    for _, char := range input {

        charx := char ^ 0x7f

        if byte(charx) == challenge[x] {
            x+=1
        } else {
            os.Exit(-1)
        }
    }
    if x == (len(challenge)-1) {
        fmt.Println(input + " is the correct flag!")
    }
}

func main() {

    if len(os.Args) < 2 {
        fmt.Println("goxor <string>")
        os.Exit(-1)
    }

    goxor(os.Args[1])
}

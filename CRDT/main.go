package main

import "fmt"

// type test struct {
// 	data_to_request string
// }

type CRDT struct {
	P     map[string]int
	N     map[string]int
	tests map[string][]string
}

func do_test(tests []string) bool {
	// Perform test by requesting proof of storage

	return true
}

func max(a int, b int) int {
	if a > b {
		return a
	} else {
		return b
	}
}

func (A *CRDT) merge(B CRDT) {
	for index, _ := range A.P {
		if do_test(B.tests[index]) {
			A.P[index] = max(A.P[index], B.P[index])
		}
	}
	for index, _ := range A.N {
		if do_test(B.tests[index]) {
			B.N[index] = max(A.N[index], B.N[index])
		}
	}
	// Still need to implement the merging of tests
}

func main() {
	var A CRDT
	var B CRDT

	A.P = map[string]int{}
	B.P = map[string]int{}
	B.tests = map[string]string{}

	B.tests["134.214.202.21"] = append(B.tests["134.214.202.21"], "data1")
	B.tests["134.214.202.22"] = append(B.tests["134.214.202.22"], "data1")
	B.tests["134.214.202.23"] = append(B.tests["134.214.202.23"], "data1")

	A.P["134.214.202.21"] = 3
	A.P["134.214.202.22"] = 5
	A.P["134.214.202.23"] = 7

	B.P["134.214.202.21"] = 2
	B.P["134.214.202.22"] = 2
	B.P["134.214.202.23"] = 10

	fmt.Println(A)
	fmt.Println(B)

	A.merge(B)

	fmt.Println(A)

}

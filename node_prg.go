package main

import (
	"bufio"
	"fmt"
	"net"
	"sync"
)

var wg sync.WaitGroup

func main() {
	defer wg.Done()
	fmt.Printf("Starting peer program\n")
	wg.Add(1)
	go acceptConnections()
	wg.Wait()

}

func acceptConnections() {
	fmt.Println("Attempting to start listening ... ")
	l, err := net.Listen("tcp", "localhost:60000")
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Now listening to potential peers on port 60000")

	defer l.Close()
	for {
		fmt.Println("Accepting connections on port 60000")
		conn, errconn := l.Accept()
		if errconn != nil {
			fmt.Println("Error while accepting connections")
			return
		}

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	for {
		message, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Printf("%s\n", message)
		if message == "hello\n" {
			fmt.Println("Peer attempting connection ...")
		} else {
			fmt.Println("Message unrecognized - ignoring msg")
		}
	}
}

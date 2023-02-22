package main

import (
	"bufio"
	"fmt"
	"net"
	"sync"
)

var wg sync.WaitGroup
var peers []string

func main() {
	defer wg.Done()
	fmt.Printf("Starting peer program\n")
	wg.Add(1)
	//go acceptConnections()

	addNewPeer("localhost:60000")

}

func acceptConnections() {
	fmt.Println("Attempting to start listening ... ")
	l, err := net.Listen("tcp", "localhost:60001")
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Now listening to potential peers on port 60001")

	defer l.Close()
	for {
		fmt.Println("Accepting connections on port 60001")
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
		if message == "hello-23\n" {
			fmt.Println("Peer attempting connection ...")
			bufio.NewWriter(conn).WriteString("connect-ok\n")
			peers = append(peers, conn.RemoteAddr().String())
			fmt.Println(peers)
		} else {
			fmt.Println("Message unrecognized - ignoring msg")
		}
	}
}

func addNewPeer(add string) {
	fmt.Println("Adding new peer", add)

	conn1, err := net.Dial("tcp", add)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn1.Close()
	sent := bufio.NewWriter(conn1)
	sent.WriteString("hello-23\n")
	sent.Flush()

	message, _ := bufio.NewReader(conn1).ReadString('\n')

	if message == "connect-ok\n" {
		fmt.Println("Peer accepted connection - adding peer to peers")
		peers = append(peers, add)
		fmt.Println(peers)
	}

}

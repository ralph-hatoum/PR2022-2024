package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"sync"
)

var wg sync.WaitGroup
var peers []string

func main() {
	defer wg.Done()
	fmt.Printf("Starting peer program\n")
	//wg.Add(1)
	//go acceptConnections()
	wg.Add(1)
	go addNewPeer("localhost:60000")
	wg.Wait()

}

func acceptConnections() {
	fmt.Println("Attempting to start listening ... ")
	l, err := net.Listen("tcp", "localhost:60001")
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
	fmt.Println("New connection detected")

	message, _ := bufio.NewReader(conn).ReadString('\n')
	fmt.Printf("%s\n", message)
	if message == "hello-23\n" {
		// New peer joining the network
		handleNewPeerConn(conn)
	} else {
		fmt.Println("Message unrecognized - ignoring msg")
		fmt.Println(peers)
	}

}

func handleNewPeerConn(conn net.Conn) {

	fmt.Println("Peer attempting connection ...")
	bufio.NewWriter(conn).WriteString("connect-ok\n")
	remote_addr := conn.RemoteAddr().String()[:strings.IndexByte(conn.RemoteAddr().String(), ':')]
	if !(alreadyPeer(peers, remote_addr)) {
		peers = append(peers, remote_addr)
	} else {
		fmt.Println("Peer was already known")
	}
	fmt.Println("Peers :", peers)
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

func alreadyPeer(peers []string, peer string) bool {
	found := false
	for _, v := range peers {
		if v == peer {
			found = true
			break
		}
	}
	return found
}

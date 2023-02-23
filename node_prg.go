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
	// Main program
	defer wg.Done()
	fmt.Printf("Starting peer program\n")
	wg.Add(1)
	go acceptConnections()
	wg.Wait()

}

func acceptConnections() {
	// Node is constantly listening to its peers - this function sets up a tcp server and accepts connections
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
	// This function handles the connection - there are several reasons as to why a node would want to contact its peers, so here we distinguish between those
	// A node can either :
	// - Start a new connection or join the network
	// - Ask for storage space
	// - Ask for the status of its data on a given node
	// - Ask for data to be deleted
	defer conn.Close()
	fmt.Println("New connection detected")

	message, _ := bufio.NewReader(conn).ReadString('\n')
	fmt.Printf("%s\n", message)
	if message == "hello-23\n" {
		// New peer joining the network
		handleNewPeerConn(conn)
	} else {
		// Unrecognized message
		fmt.Println("Message unrecognized - ignoring msg")
		fmt.Println(peers)
	}

}

func handleNewPeerConn(conn net.Conn) {
	// Executed when a new peer connects to us - we send him a conformation with "connect-ok"
	// and if the peer was not already in our known peers, we add him to the known peers
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
	// This function a node to initiate a connection to another peer
	// most likely will only be used once when the node is turned on, and only again if the node goes down and wants to come back to the network
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
		fmt.Println("Peer accepted connection")
		if alreadyPeer(peers, add) {
			fmt.Println("Peer was already known")
		} else {
			peers = append(peers, add)
			fmt.Println("Added peer to the network")
		}
		fmt.Println(peers)
	}

}

func alreadyPeer(peers []string, peer string) bool {
	// checks if the peer is already known
	found := false
	for _, v := range peers {
		if v == peer {
			found = true
			break
		}
	}
	return found
}

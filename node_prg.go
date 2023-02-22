package main

import (
	"fmt"
	"net"
)

func main() {
	fmt.Println("Starting peer program")
	go acceptConnections()

}

func acceptConnections() {
	l, err := net.Listen("tcp", "60000")
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
			fmt.Println(errconn)
			return
		}

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {

}

package main

import (
	"bufio"
	"crypto/sha256"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"net"
	"os"
	"os/exec"
	"strings"
	"sync"
	"time"
)

var wg sync.WaitGroup
var peers []string
var files []string

type file_at_peer struct {
	file_name   string
	peer_adress string
}

var files_at_peers []file_at_peer

func main() {
	// Main program
	defer wg.Done()
	fmt.Printf("Starting peer program\n")
	wg.Add(1)
	go acceptConnections()
	wg.Add(1)
	go watchFS()
	wg.Add(1)
	go sendFilesToPeer()
	wg.Add(1)
	go checkOnFiles()
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

	message_buffer := bufio.NewReader(conn)
	message, err := message_buffer.ReadString('\n')
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("%s\n", message)
	if message == "hello-23\n" {
		// New peer joining the network
		handleNewPeerConn(conn)
	} else if message == "storage-request\n" {
		file_name, _ := message_buffer.ReadString('\n')
		fmt.Println(file_name)
		receiveFile(conn, file_name)
	} else if message[:9] == "CheckFile" {
		fmt.Println("Checkfile request received")
		check := strings.Split(message, "-")
		fmt.Println(check)
		handleCheck(check)
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
	// can also be used to check if element is in list
	found := false
	for _, v := range peers {
		if v == peer {
			found = true
			break
		}
	}
	return found
}

func watchFS() {
	// to detect  new files in the FS

	last_status := ""

	for {
		time.Sleep(2000000000)
		//fmt.Println("Searching for new files ...")
		cmd := exec.Command("ls", "./")
		out, err := cmd.Output()

		if err != nil {
			fmt.Println(err)
			return
		}

		//fmt.Printf("%s\n", out)

		if string(out) != last_status {
			fmt.Printf("Last status : %s\n", last_status)
			fmt.Printf("Current status :\n%s\n", out)
			fmt.Println("Change in FS detected ")
			fmt.Println("\n")
			last_status = string(out)
			go updateFiles(string(out))

		}

	}

}

func updateFiles(file_list string) {
	// any new files are added to the list of followed files
	to_check := strings.Split(file_list, "\n")

	fmt.Println(to_check)
	for _, element := range to_check {
		if !alreadyPeer(files, element) {
			file := file_at_peer{file_name: element, peer_adress: "NO_PEER"}
			files = append(files, element)
			files_at_peers = append(files_at_peers, file)
		}
	}

	fmt.Println("Files followed : ", files)
	fmt.Println("Files at peers : ", files_at_peers)
}

func sendFilesToPeer() {
	// periodically checks for unbacked up files and sends them to peers
	for {
		time.Sleep(10000000000)
		if len(files_at_peers) != 0 {
			if len(peers) != 0 {
				for index, file := range files_at_peers {
					if file.peer_adress == "NO_PEER" {

						fmt.Println("Sending file to peer ...", peers[0])

						sendFileToPeer(file.file_name, peers[0])

						(&files_at_peers[index]).peer_adress = peers[0]

					} else {
						fmt.Println("File already backed at peer", file.peer_adress)
					}
				}
			} else {
				fmt.Println("No peers to communicate with ! ")
			}
		}
	}
}

func sendFileToPeer(file_name string, peer_address string) {

	// to send a file to a peer
	conn, err := net.Dial("tcp", peer_address+":60001")

	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	message := bufio.NewWriter(conn)
	message.WriteString("storage-request\n")
	message.Flush()

	//file_name_to_send := bufio.NewWriter(conn)
	fmt.Println("Sending file : ", file_name+"\n")
	message.WriteString(file_name + "\n")
	message.Flush()

	fi, err := os.Open("./" + file_name)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer fi.Close()

	_, err = io.Copy(conn, fi)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("File sent to ", peer_address)
}

func receiveFile(conn net.Conn, filename string) {
	//fmt.Println(filename[:len(filename)-1])
	fo, err := os.Create(filename[:len(filename)-1])
	if err != nil {
		fmt.Println(err)
		return
	}
	defer fo.Close()

	_, err = io.Copy(fo, conn)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Received file ")

}

func checkOnFiles() {
	for {
		time.Sleep(10000000000)
		for _, file := range files_at_peers {
			if file.peer_adress != "NO_PEER" {
				nonce := rand.Float64()
				h := sha256.New()
				file_content, err := ioutil.ReadFile(file.file_name)
				if err != nil {
					fmt.Println(err)
					return
				}
				nonce_str := fmt.Sprintf("%f", nonce)
				nonce_bytes := []byte(nonce_str)
				for _, nonce_byte := range nonce_bytes {
					file_content = append(file_content, nonce_byte)
				}
				h.Write(file_content)
				expected_result := h.Sum(nil)
				fmt.Printf("Expected result for file %s : %x\n", file.file_name, expected_result)
				conn, err := net.Dial("tcp", file.peer_adress+":60001")
				if err != nil {
					fmt.Println(err)
					return
				}
				message := bufio.NewWriter(conn)
				message.WriteString("CheckFile-" + file.file_name + "-" + string(nonce_str) + "\n")
				message.Flush()

			}
		}
	}
}

func handleCheck(check []string) {
	file_name := check[1]
	nonce := check[2]
	h := sha256.New()
	file_content, err := ioutil.ReadFile(file_name)

	if err != nil {
		fmt.Println(err)
		return
	}

	nonce_bytes := []byte(nonce)
	for _, nonce_byte := range nonce_bytes {
		file_content = append(file_content, nonce_byte)
	}
	h.Write(file_content)
	result := h.Sum(nil)

	fmt.Println(result)

}

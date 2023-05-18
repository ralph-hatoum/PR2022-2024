package main

import (
	"bufio"
	"crypto"
	"fmt"
	"net"
	"strings"
	"sync"
	"ecdh"
)

const port = "60000"
const port_to_contact = "60001"

var wg sync.WaitGroup

var commonKey = ""

type peer struct {
	peer_address string
}

var peers []peer

func main() {
	// Main program
	defer wg.Done()
	fmt.Printf("Starting peer program\n")
	wg.Add(1)
	go acceptConnections()
	wg.Add(1)
	go addNewPeer("127.0.0.1:" + port_to_contact)
	wg.Wait()

}

func acceptConnections() {
	// Node is constantly listening to its peers - this function sets up a tcp server and accepts connections
	fmt.Println("Attempting to start listening ... ")
	l, err := net.Listen("tcp", "127.0.0.1:"+port)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Now listening to potential peers on port" + port)

	defer l.Close()
	for {
		fmt.Println("Accepting connections on port " + port)
		conn, errconn := l.Accept()
		if errconn != nil {
			fmt.Println("Error while accepting connections")
			return
		}

		handleConnection(conn)

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
	} else {
		// Unrecognized message
		fmt.Println("Message unrecognized - ignoring msg")
		fmt.Println(peers)
	}

}

func handleNewPeerConn(conn net.Conn) {
	// Executed when a new peer connects to us - we send him a conformation with "connect-ok"
	// and if the peer was not already in our known peers, we add him to the known peers
	fmt.Printf("\n")
	fmt.Println("Peer attempting connection ...")
	fmt.Printf("\n")
	to_send := bufio.NewWriter(conn)
	to_send.WriteString("connect-ok\n")
	to_send.Flush()
	remote_addr := conn.RemoteAddr().String()[:strings.IndexByte(conn.RemoteAddr().String(), ':')]
	if !(alreadyPeer(peers, remote_addr)) {
		new_peer := peer{peer_address: remote_addr}
		peers = append(peers, new_peer)
		if commonKey == "" {
			generateCommonKey(new_peer)
		}
	} else {
		fmt.Println("Peer was already known")
	}
	fmt.Println("Peers :", peers)
}

func addNewPeer(add string) {
	// This function a node to initiate a connection to another peer
	// most likely will only be used once when the node is turned on, and only again if the node goes down and wants to come back to the network
	fmt.Printf("\n")
	fmt.Println("Adding new peer", add)
	fmt.Printf("\n")

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
		if alreadyPeer(peers, add[:strings.IndexByte(add, ':')]) {
			fmt.Printf("\n")
			fmt.Println("Peer was already known")
			fmt.Printf("\n")
		} else {
			new_peer := peer{peer_address: add[:strings.IndexByte(add, ':')]}
			peers = append(peers, new_peer)
			fmt.Printf("\n")
			fmt.Println("Added peer to the network")
			fmt.Printf("\n")
		}
		fmt.Println(peers)
	} else {
		fmt.Println("No response from ", add)
	}

}

func alreadyPeer(peers []peer, peer string) bool {
	// checks if the peer is already known
	// can also be used to check if element is in list
	found := false
	for _, v := range peers {
		if v.peer_address == peer || v.peer_address == "localhost" && peer == "127.0.0.1" || peer == "localhost" && v.peer_address == "127.0.0.1" {
			found = true
			break
		}
	}
	return found
}

func generateCommonKey(peer peer) {
	conn, err := net.Dial("tcp", peer.peer_address)
	if err != nil {
		fmt.Println(err)
		return
	}
	write_buffer := bufio.NewWriter(conn)
	msg := "gen-common-key\n"
	write_buffer.WriteString(msg)
	write_buffer.Flush()

	read_buffer := bufio.NewReader(conn)
	response, err := read_buffer.ReadString('\n')
	if response == "gen-common-key-ok" {
		key_exchange := 
	} else {
		fmt.Println("Error : peer not willing to generate key")
	}



}

// func watchFS() {
// 	// to detect  new files in the FS

// 	last_status := ""

// 	for {
// 		time.Sleep(2000000000)
// 		//fmt.Println("Searching for new files ...")
// 		cmd := exec.Command("ls", "./to_share")
// 		out, err := cmd.Output()

// 		if err != nil {
// 			fmt.Println(err)
// 			return
// 		}

// 		//fmt.Printf("%s\n", out)

// 		if string(out) != last_status {
// 			fmt.Printf("Last status : %s\n", last_status)
// 			fmt.Printf("Current status :\n%s\n", out)
// 			fmt.Println("Change in FS detected ")
// 			fmt.Println("\n")
// 			last_status = string(out)
// 			go updateFiles(string(out))

// 		}

// 	}

// }

// func updateFiles(file_list string) {
// 	// any new files are added to the list of followed files
// 	to_check := strings.Split(file_list, "\n")
// 	to_check = to_check[0 : len(to_check)-1]

// 	//fmt.Println(to_check)
// 	for _, element := range to_check {
// 		if !inList(files, element) {
// 			file := file_at_peer{file_name: element, peer_adress: "NO_PEER"}
// 			files = append(files, element)
// 			files_at_peers = append(files_at_peers, file)
// 		}
// 	}
// 	fmt.Printf("\n")

// 	fmt.Println("Files followed : ", files)
// 	fmt.Printf("\n")
// 	fmt.Println("Files at peers : ", files_at_peers)
// 	fmt.Printf("\n")
// }

// func sendFilesToPeer() {
// 	// periodically checks for unbacked up files and sends them to peers
// 	for {
// 		time.Sleep(1000000)
// 		if len(files_at_peers) != 0 {
// 			if len(peers) != 0 {
// 				for index, file := range files_at_peers {
// 					if file.peer_adress == "NO_PEER" {
// 						best_peers := chooseBestPeers(peers)
// 						chosen_peer := best_peers[0]
// 						fmt.Println("Sending file to peer ...", chosen_peer)

// 						res := sendFileToPeer(file.file_name, chosen_peer.peer_address)

// 						if res {
// 							(&files_at_peers[index]).peer_adress = chosen_peer.peer_address
// 						} else {
// 							fmt.Println("Could not send file to peer")
// 						}

// 					}
// 				}
// 			} else {
// 				fmt.Println("No peers to communicate with ! ")
// 			}
// 		}
// 	}
// }

// func sendFileToPeer(file_name string, peer_address string) bool {

// 	// to send a file to a peer
// 	conn, err := net.Dial("tcp", peer_address+":"+port_to_contact)

// 	if err != nil {
// 		fmt.Println(err)
// 		return false
// 	}
// 	defer conn.Close()

// 	message := bufio.NewWriter(conn)
// 	message.WriteString("storage-request\n")
// 	message.Flush()

// 	//file_name_to_send := bufio.NewWriter(conn)
// 	fmt.Println("Sending file : ", file_name+"\n")
// 	message.WriteString(file_name + "\n")
// 	message.Flush()

// 	fi, err := os.Open("./to_share/" + file_name)
// 	if err != nil {
// 		fmt.Println(err)
// 		return false
// 	}
// 	defer fi.Close()

// 	_, err = io.Copy(conn, fi)
// 	if err != nil {
// 		fmt.Println(err)
// 		return false
// 	}

// 	fmt.Println("File sent to ", peer_address)
// 	for index, peer := range peers {
// 		if peer.peer_address == peer_address {
// 			if inList(peer.files, file_name) {
// 				fmt.Println("Peer's file list already contained required information -- did not update")
// 			} else {
// 				(&peers[index]).files = append(peer.files, file_name)
// 				fmt.Println("Updated peer's file list")
// 			}

// 		}
// 	}
// 	return true
// }

// func receiveFile(conn net.Conn, filename string, peer string) {
// 	//fmt.Println(filename[:len(filename)-1])
// 	fo, err := os.Create("./" + peer[:strings.IndexByte(peer, ':')] + "/" + filename[:len(filename)-1])
// 	if err != nil {
// 		fmt.Println(err)
// 		return
// 	}
// 	defer fo.Close()

// 	_, err = io.Copy(fo, conn)
// 	if err != nil {
// 		fmt.Println(err)
// 		return
// 	}

// 	fmt.Println("Received file ")

// }

// func checkOnFiles() {
// 	for {
// 		time.Sleep(10000000000)
// 		fmt.Println("Peers : ", peers)
// 		for index, peer := range peers {
// 			//fmt.Println("Checking files on peer ", peer)
// 			number_of_checks := 0.0
// 			number_of_ok_checks := 0.0
// 			for _, file := range peer.files {

// 				nonce := rand.Float64()
// 				h := sha256.New()
// 				file_content, err := ioutil.ReadFile("./to_share/" + file)
// 				if err != nil {
// 					fmt.Println(err)
// 					return
// 				}
// 				nonce_str := fmt.Sprintf("%f", nonce)
// 				nonce_bytes := []byte(nonce_str)
// 				for _, nonce_byte := range nonce_bytes {
// 					file_content = append(file_content, nonce_byte)
// 				}
// 				h.Write(file_content)
// 				//fmt.Printf("Hashing buffer : %x\n", file_content)
// 				expected_result := h.Sum(nil)
// 				expected_result_string := fmt.Sprintf("%x", expected_result)
// 				//fmt.Printf("Expected result for file %s with nonce %s : %x\n", file.file_name, nonce_str, expected_result)
// 				conn, err := net.Dial("tcp", peer.peer_address+":"+port_to_contact)
// 				if err != nil {
// 					fmt.Println(err)
// 					return
// 				}
// 				message := bufio.NewWriter(conn)
// 				message.WriteString("CheckFile-" + file + "-" + string(nonce_str) + "\n")
// 				message.Flush()
// 				start := time.Now()
// 				received_check_buffer := bufio.NewReader(conn)
// 				received_check, err := received_check_buffer.ReadString('\n')
// 				elapsed := time.Since(start)

// 				if err != nil {
// 					fmt.Println(err)
// 					return
// 				}
// 				received_check = received_check[0 : len(received_check)-1]

// 				number_of_checks += 1

// 				if received_check == expected_result_string {
// 					number_of_ok_checks += 1
// 					//fmt.Printf("\n")
// 					//fmt.Printf("\n")
// 					//fmt.Printf("Check on %s ok !\n", file)
// 					//fmt.Printf("Node response time : %s\n", elapsed)
// 					//fmt.Printf("\n")
// 					//fmt.Printf("\n")

// 					(&peers[index]).peer_avg_resp_time = peer.peer_avg_resp_time/2 + int(elapsed)
// 					//fmt.Println("Updated average response time for peer :")
// 					//fmt.Println(peer)

// 					//fmt.Printf("\n")
// 					//fmt.Printf("\n")
// 				} else {
// 					//fmt.Printf("\n")
// 					//fmt.Printf("\n")
// 					fmt.Printf("File check on %s failed \n", file)
// 					fmt.Printf("Expected : %x\n", expected_result)
// 					//fmt.Println("Resending file")
// 					//fmt.Printf("\n")
// 					//fmt.Printf("\n")
// 					fmt.Println("Resending file")
// 					sendFileToPeer(file, peer.peer_address)

// 				}

// 			}

// 			reliability := number_of_ok_checks / number_of_checks

// 			fmt.Println("Peer's ratio : ", reliability)

// 			(&peers[index]).peer_score = 0.3*(&peers[index]).peer_score + 0.7*reliability

// 		}
// 	}
// }

// func handleCheck(check []string, peer string) []byte {
// 	fmt.Println("HANDLING CHECK for peer ", peer)
// 	file_name := check[1]
// 	fmt.Println("file :", file_name)
// 	nonce := check[2]
// 	fmt.Println("nonce :", nonce)
// 	h := sha256.New()
// 	file_content, err := ioutil.ReadFile("./" + peer + "/" + file_name)

// 	if err != nil {
// 		fmt.Println(err)
// 		fmt.Println("File could not be found")
// 		// TODO HANDLE FILE LOSS SIGNAL
// 	}

// 	//fmt.Println(file_content)

// 	nonce_bytes := []byte(nonce)
// 	for _, nonce_byte := range nonce_bytes {
// 		file_content = append(file_content, nonce_byte)
// 	}
// 	//fmt.Printf("Hashing buffer : %x\n", file_content[0:len(file_content)-1])
// 	h.Write(file_content[0 : len(file_content)-1])
// 	result := h.Sum(nil)

// 	fmt.Printf("Result for file %s : %x\n", file_name, result)

// 	return result

// }

// func inList(l []string, s string) bool {
// 	found := false
// 	for _, v := range l {
// 		if v == s {
// 			found = true
// 			break
// 		}
// 	}
// 	return found
// }

// func chooseBestPeers(peers []peer) []peer {
// 	// Function to choose best peer current peer
// 	// default value for n should be 1

// 	if len(peers) == 0 {
// 		fmt.Println("No peers ! Please connect to the network")
// 		panic(0)
// 	} else if len(peers) == 1 {
// 		fmt.Println("Only in communication with one peer")
// 		return []peer{peers[0]}
// 	}
// 	max_resp_time := peers[0]
// 	max_reliability := peers[0]
// 	for _, peer := range peers {
// 		if peer.peer_avg_resp_time < max_resp_time.peer_avg_resp_time {
// 			max_resp_time = peer
// 		}
// 		if peer.peer_score > max_reliability.peer_score {
// 			max_reliability = peer
// 		}
// 	}

// 	return []peer{max_reliability, max_resp_time}

// }

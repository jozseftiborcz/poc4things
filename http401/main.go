package main

import (
	"fmt"
	"log"
	"net/http"
	"encoding/base64"
)

const (
	username = "admin"
	password = "password"
)

func loginHandler(w http.ResponseWriter, r *http.Request) {
	// Check if Authorization header is present
	auth := r.Header.Get("Authorization")
	if auth == "" {
		// Authorization header missing, send 401 Unauthorized response with WWW-Authenticate header
		w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Check if the provided credentials match
	valid := checkCredentials(auth)
	if !valid {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Credentials are valid, send a personalized greeting
	greet := fmt.Sprintf("Hello, %s!", username)
	w.Write([]byte(greet))
}

func checkCredentials(auth string) bool {
	// Extract credentials from Authorization header
	credentials := auth[len("Basic "):]
	decodedCreds, err := decodeBase64(credentials)
	if err != nil {
		return false
	}

	// Check if the credentials match the expected username and password
	return decodedCreds == username+":"+password
}

func decodeBase64(s string) (string, error) {
	bytes, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		return "", err
	}
	return string(bytes), nil
}

func main() {
	http.HandleFunc("/login", loginHandler)
	log.Println("Server listening on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}


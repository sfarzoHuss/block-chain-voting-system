// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

contract UserContract {

    // Contract's Owner address
    address public votation;

    // Struct to represent user data
    struct User {
        bytes32 name;
        bytes32 lastname;
        bytes32 email;
        bytes32 passwordHash;
        bytes32 salt;
        bool registered;
        bool is_admin;
    }

    // Mapping to store users
    mapping (bytes32 => User) public users;

    // Event to log user registration
    event UserRegistered(bytes32 uniqueCode, bytes32 email);

    // Event to log user login
    event UserLoggedIn(address indexed userAddress);

    // Modifier to check if the user is registered
    modifier onlyRegisteredUser(bytes32 _email, bytes32 _password) {

        // Generate a unique code using the election's address and timestamp
        bytes32 uniqueCode = keccak256(abi.encodePacked(msg.sender, _email));

        require(users[uniqueCode].registered, "User not registered");
        _;
    }

    constructor() {
        // Set owner to contract deployer.
        votation = msg.sender;
    }

    // User registration function
    function register(bytes32 _name, bytes32 _lastname, bytes32 _email, bytes32 _password, bool _isadmin) public {

        // Generate a unique code using the election's address and timestamp
        bytes32 uniqueCode = keccak256(abi.encodePacked(msg.sender, _email));

        // Check if the user is not already registered
        require(!users[uniqueCode].registered, "User already registered");

        // Generate a random salt for password hashing
        bytes32 salt = bytes32(block.timestamp);

        // Hash the password with the salt
        bytes32 passwordHash = keccak256(abi.encodePacked(_password, salt));

        // Create a new user
        User memory newUser = User({
            name: _name,
            lastname: _lastname,
            email: _email,
            passwordHash: passwordHash,
            salt: salt,
            registered: true,
            is_admin: _isadmin
        });

        // Store the user in the mapping
        users[uniqueCode] = newUser;

        // Emit registration event
        emit UserRegistered(uniqueCode, _email);
    }

    // User login function
    function login(bytes32 _email, bytes32 _password) public onlyRegisteredUser(_email, _password) {

        // Generate a unique code using the election's address and email
        bytes32 id_user = keccak256(abi.encodePacked(msg.sender, _email));

        // Hash the provided password with the stored salt
        bytes32 hashedPassword = keccak256(abi.encodePacked(_password, users[id_user].salt));

        // Check if the provided password hash matches the stored password hash
        require(users[id_user].passwordHash == hashedPassword, "Invalid credentials");

        // Emit login event
        emit UserLoggedIn(msg.sender);

    }

    // Get user information
    function getUserInfo(bytes32 _email) public view returns (bytes32, bytes32, bool) {
        // Generate a unique code using the election's address and timestamp
        bytes32 id_user = keccak256(abi.encodePacked(msg.sender, _email));
        return (users[id_user].name, users[id_user].lastname, users[id_user].is_admin);
    }
}


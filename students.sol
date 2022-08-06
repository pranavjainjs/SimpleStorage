// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract student{

    uint public n = 0;

    struct Stud {
        uint roll;
        string name;
        string branch;
        string email;
    }

    Stud[] public studs;
    mapping(uint => Stud) public listOfStuds;
    // string is address of deployed smart contract?

    function addStud(uint _roll, string memory _name, string memory _branch, string memory _email, uint _index) public{
        studs.push(Stud(_roll, _name, _branch, _email));
        listOfStuds[_roll] = studs[_index];
    }

    function retrieve(uint _roll) public view returns (string memory _name, string memory _branch, string memory _email) {
        return ( listOfStuds[_roll].name, listOfStuds[_roll].branch, listOfStuds[_roll].email);
    }
}

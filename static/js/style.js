// queryFetch(`
//  query{
// 	 allUsers {
// 	   id
// 	   imie
// 	   nazwisko
// 	   dataZalozenia
// 	}
//   }
// `)

// function queryFetch(query) {
// 	return fetch('http://127.0.0.1:8000/graphql/',{
// 	method: 'POST',
// 	headers: {"Content-type": "application/json" },
// 	body: JSON.stringify({
// 		query: query
// 	})
// }).then(res => console.log(res.json()))
// }

fetch('http://127.0.0.1:8000/graphql/', {
  method: 'POST',
  Authorization: "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikt1YmFsb25layIsImV4cCI6MTU5NDcyMTk4NCwib3JpZ0lhdCI6MTU5NDcyMTY4NH0.z1rZNLUgQkhK7R-gge-tG2l_5RY4V06HnEs1zSU1gYE"
 	headers: {"Content-type": "application/json" },
 	body: JSON.stringify({
        mutation:
         `
         mutation{
            tokenAuth(username: "Kubalonek", password: ""){
              token
            }
          }`
 	})
 }).then(res => console.log(res))


// fetch('http://127.0.0.1:8000/graphql/')
//     .then(res => res.json())
//     .then(data => console.log(data))



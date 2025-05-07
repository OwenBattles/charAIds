struct CharadesRequest: Codable {
    let category: String
}

struct CharadesResponse: Codable {
    let charades: [String]
}

func fetchCharades(for category: String, completion: @escaping ([String]) -> Void) {
    guard let url = URL(string: "https://yourdomain.com/generate-charades") else { return }
    
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = CharadesRequest(category: category)
    request.httpBody = try? JSONEncoder().encode(body)

    URLSession.shared.dataTask(with: request) { data, response, error in
        if let data = data {
            if let decoded = try? JSONDecoder().decode(CharadesResponse.self, from: data) {
                DispatchQueue.main.async {
                    completion(decoded.charades)
                }
            }
        }
    }.resume()
}

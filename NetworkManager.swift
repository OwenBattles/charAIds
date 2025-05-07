import Foundation

struct ItemResponse: Codable {
    let items: [String]
}

class NetworkManager {
    static let shared = NetworkManager()

    func fetchItems(category: String, count: Int, completion: @escaping ([String]) -> Void) {
        guard let url = URL(string: "http://127.0.0.1:5000/generate-list") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: Any] = [
            "category": category,
            "count": count
        ]

        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data else { return }
            if let decoded = try? JSONDecoder().decode(ItemResponse.self, from: data) {
                DispatchQueue.main.async {
                    completion(decoded.items)
                }
            }
        }.resume()
    }
}

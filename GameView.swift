import SwiftUI

struct GameView: View {
    @State private var items: [String] = []
    @State private var loading = false

    var body: some View {
        VStack(spacing: 20) {
            if loading {
                ProgressView("Loading...")
            } else {
                List(items, id: \.self) { item in
                    Text(item)
                }
            }

            Button("Load Category: Animals") {
                loading = true
                NetworkManager.shared.fetchItems(category: "animals", count: 10) { result in
                    self.items = result
                    self.loading = false
                }
            }
        }
        .padding()
    }
}

# **Phân Tích và Thiết Kế Hệ Thống Multi-Agent cho Review Mã Nguồn và Hỗ Trợ Phát Triển Phần Mềm**

## **I. Giới thiệu**

Trong bối cảnh phát triển phần mềm hiện đại, việc đảm bảo chất lượng, bảo mật và kiến trúc của mã nguồn là một thách thức không ngừng gia tăng. Các quy trình review mã nguồn thủ công thường tốn thời gian, dễ bỏ sót lỗi và khó có thể bao quát toàn bộ các khía cạnh phức tạp của một dự án lớn. Để giải quyết những vấn đề này, việc ứng dụng các hệ thống thông minh, tự động hóa đang trở thành một xu hướng tất yếu. Báo cáo này trình bày một phân tích chi tiết và đề xuất thiết kế cho một hệ thống Multi-Agent (MAS) tiên tiến, có khả năng tự động hóa các tác vụ review mã nguồn, phân tích Pull Request (PR), và hỗ trợ nhà phát triển thông qua cơ chế hỏi đáp tương tác về cơ sở mã.

Hệ thống được đề xuất sẽ tận dụng sức mạnh của các Mô hình Ngôn ngữ Lớn (LLM) kết hợp với một loạt các công cụ mã nguồn mở chuyên dụng cho việc phân tích mã. Nền tảng cốt lõi của hệ thống dựa trên các công nghệ do Google phát triển, bao gồm Agent Development Kit (ADK) để xây dựng các tác tử (agent), Model Context Protocol (MCP) để chuẩn hóa giao tiếp giữa tác tử và công cụ, và Agent2Agent Protocol (A2A) để điều phối sự hợp tác giữa nhiều tác tử. Mục tiêu là xây dựng một hệ thống linh hoạt, có khả năng mở rộng và dễ dàng tích hợp vào các quy trình phát triển phần mềm hiện có, từ đó nâng cao năng suất, chất lượng sản phẩm và giảm thiểu rủi ro bảo mật.

## **II. Yêu cầu Chức năng Cốt lõi**

Hệ thống Multi-Agent cần đáp ứng các yêu cầu chức năng chính sau đây để phục vụ hiệu quả cho quá trình phát triển và bảo trì phần mềm:

1. **Review toàn diện mã nguồn:**  
   * Hệ thống phải có khả năng phân tích mã nguồn từ các kho lưu trữ Git (ví dụ: GitHub) hoặc từ các tệp cục bộ.  
   * Phát hiện các lỗ hổng bảo mật tiềm ẩn (security vulnerabilities).  
   * Xác định các vấn đề liên quan đến kiến trúc phần mềm (architecture flaws), chẳng hạn như vi phạm các nguyên tắc thiết kế, các anti-pattern, hoặc các phụ thuộc không mong muốn.  
2. **Review Pull Request (PR) thông minh:**  
   * Tự động phân tích các thay đổi trong một PR để phát hiện lỗi cú pháp, lỗi logic, và các vấn đề tiềm ẩn khác.  
   * Liệt kê các thành phần, module, hoặc chức năng trong mã nguồn có khả năng bị ảnh hưởng bởi những thay đổi trong PR. Điều này giúp định hướng cho việc kiểm thử hồi quy (regression testing) nhằm tránh các hiệu ứng phụ (side-effects).  
3. **Hỏi đáp và tương tác về mã nguồn:**  
   * Cung cấp một giao diện cho phép người dùng (nhà phát triển) đặt câu hỏi về cơ sở mã.  
   * Có khả năng tạo ra các biểu đồ trực quan hóa cấu trúc mã nguồn, ví dụ như sơ đồ trình tự (sequence diagram) và sơ đồ lớp (class diagram), dựa trên yêu cầu của người dùng.  
   * Đưa ra các gợi ý, đề xuất để cải thiện hoặc sửa đổi mã nguồn, dựa trên các phân tích đã thực hiện hoặc các truy vấn của người dùng.

Ngoài các chức năng cốt lõi trên, hệ thống cần được xây dựng dựa trên các tiêu chí sau:

* **Ưu tiên sử dụng công cụ mã nguồn mở:** Tận dụng các thư viện và công cụ mã nguồn mở đã được cộng đồng kiểm chứng cho việc quét mã, phân tích và hiểu cơ sở mã, ví dụ như PMD.  
* **Tích hợp với LLM thông qua MCP:** Các công cụ phân tích sẽ giao tiếp với các Mô hình Ngôn ngữ Lớn (LLM) thông qua Model Context Protocol (MCP), đảm bảo tính chuẩn hóa và linh hoạt trong việc mở rộng khả năng của LLM.  
* **Phát triển tác tử dựa trên ADK:** Các tác tử (agent) trong hệ thống sẽ được phát triển bằng Agent Development Kit (ADK) của Google, một framework linh hoạt và module hóa cho việc xây dựng và triển khai tác tử AI.1  
* **Giao tiếp đa tác tử qua A2A:** Nhiều tác tử sẽ tương tác và phối hợp với nhau thông qua Agent2Agent Protocol (A2A), một tiêu chuẩn mở do Google phát triển để cho phép giao tiếp liền mạch giữa các tác tử AI.2

## **III. Kiến trúc Hệ thống Đề xuất**

Để đáp ứng các yêu cầu đã nêu, một kiến trúc hệ thống Multi-Agent (MAS) được đề xuất, tập trung vào tính module, khả năng mở rộng và sự phối hợp hiệu quả giữa các thành phần chuyên biệt.

### **A. Tổng quan Kiến trúc Đa Tác tử (Multi-Agent System \- MAS)**

Hệ thống được thiết kế như một tập hợp các tác tử (agent) chuyên biệt, mỗi tác tử chịu trách nhiệm thực hiện một nhóm chức năng cụ thể. Các tác tử này sẽ hợp tác với nhau để hoàn thành các yêu cầu phức tạp từ người dùng hoặc từ các hệ thống CI/CD. Kiến trúc MAS mang lại nhiều lợi thế, bao gồm tính module cao, khả năng chuyên môn hóa, tái sử dụng, bảo trì dễ dàng và khả năng định nghĩa các luồng kiểm soát có cấu trúc.1

Một tác tử điều phối trung tâm (Orchestrator Agent) sẽ chịu trách nhiệm tiếp nhận yêu cầu, phân rã thành các nhiệm vụ nhỏ hơn và giao cho các tác tử chuyên biệt phù hợp. Các tác tử chuyên biệt sẽ thực thi nhiệm vụ của mình, có thể sử dụng các công cụ mã nguồn mở và LLM, sau đó trả kết quả về cho tác tử điều phối để tổng hợp và phản hồi lại người dùng.

### **B. Các Thành phần Chính và Luồng Tương tác**

Sơ đồ dưới đây minh họa kiến trúc tổng thể của hệ thống và luồng tương tác chính giữa các thành phần:

Code snippet

graph TD  
    User \--\>|Yêu cầu| OA(Orchestrator Agent \- ADK)

    subgraph "Hệ thống Multi-Agent"  
        OA \--\>|A2A Task| CRA(Code Retrieval Agent \- ADK)  
        OA \--\>|A2A Task| SA(Static Analysis Agent \- ADK)  
        OA \--\>|A2A Task| SCAA(SCA Agent \- ADK)  
        OA \--\>|A2A Task| PRIA(PR Review & Impact Analysis Agent \- ADK)  
        OA \--\>|A2A Task| DGA(Diagram Generation Agent \- ADK)  
        OA \--\>|A2A Task| CSA(Code Suggestion Agent \- ADK)  
        OA \--\>|A2A Task| QAA(Q\&A Agent \- ADK)

        CRA \--\>|Code Path/Data via A2A| OA  
        SA \--\>|Kết quả SAST via A2A| OA  
        SCAA \--\>|Kết quả SCA via A2A| OA  
        PRIA \--\>|Kết quả Phân tích PR via A2A| OA  
        DGA \--\>|Sơ đồ via A2A| OA  
        CSA \--\>|Gợi ý Mã via A2A| OA  
        QAA \--\>|Câu trả lời via A2A| OA  
    end

    subgraph "Công cụ & Dịch vụ Bên ngoài"  
        CRA \-.-\>|MCP Tool: Git CLI| GitRepo\[Kho Git / Filesystem\]  
        SA \-.-\>|MCP Tool: Semgrep, PMD| Codebase1\[Codebase\]  
        SCAA \-.-\>|MCP Tool: OWASP Dep-Check| Codebase2\[Codebase\]  
        PRIA \-.-\>|MCP Tool: Call Graph Tools, Diff Tools| Codebase3\[Codebase\]  
        DGA \-.-\>|MCP Tool: PlantUML, AppMap| Codebase4\[Codebase\]  
        CSA \-.-\>|MCP Tool: LLM API| LLM\_Service1  
        QAA \-.-\>|MCP Tool: LLM API, Vector DB (RAG)| LLM\_Service2 & KnowledgeBase  
    end

    OA \--\>|Phản hồi| User

    style OA fill:\#f9f,stroke:\#333,stroke-width:2px  
    style CRA fill:\#ccf,stroke:\#333,stroke-width:2px  
    style SA fill:\#ccf,stroke:\#333,stroke-width:2px  
    style SCAA fill:\#ccf,stroke:\#333,stroke-width:2px  
    style PRIA fill:\#ccf,stroke:\#333,stroke-width:2px  
    style DGA fill:\#ccf,stroke:\#333,stroke-width:2px  
    style CSA fill:\#ccf,stroke:\#333,stroke-width:2px  
    style QAA fill:\#ccf,stroke:\#333,stroke-width:2px

**Luồng tương tác chính:**

1. **Tiếp nhận yêu cầu:** Người dùng hoặc hệ thống CI/CD gửi yêu cầu đến Orchestrator Agent (OA).  
2. **Phân rã và Điều phối:** OA phân tích yêu cầu, xác định các tác tử chuyên biệt cần thiết và gửi các nhiệm vụ (task) cho chúng thông qua giao thức A2A.  
3. **Thực thi nhiệm vụ:**  
   * Các tác tử chuyên biệt (ví dụ: Static Analysis Agent, Diagram Generation Agent) nhận nhiệm vụ.  
   * Mỗi tác tử sử dụng các công cụ (tool) phù hợp, được đóng gói và truy cập thông qua MCP, để thực hiện nhiệm vụ. Ví dụ, SA Agent có thể gọi Semgrep CLI thông qua một MCP tool.  
   * Một số tác tử (ví dụ: Code Suggestion Agent, Q\&A Agent) sẽ tương tác với LLM (ví dụ: Gemini) thông qua các MCP tool chuyên dụng để tận dụng khả năng hiểu ngôn ngữ tự nhiên và sinh mã của LLM.  
4. **Tổng hợp kết quả:** Các tác tử chuyên biệt gửi kết quả thực thi nhiệm vụ trở lại OA thông qua A2A.  
5. **Phản hồi người dùng:** OA tổng hợp các kết quả, định dạng lại nếu cần, và gửi phản hồi cuối cùng cho người dùng hoặc hệ thống CI/CD.

### **C. Nền tảng Công nghệ: ADK, A2A, và MCP**

Việc lựa chọn các công nghệ của Google làm nền tảng mang lại một hệ sinh thái đồng bộ và mạnh mẽ cho việc phát triển MAS:

* **Agent Development Kit (ADK):** Là một framework linh hoạt và module hóa để phát triển và triển khai các tác tử AI.1 ADK cho phép xây dựng các ứng dụng phức tạp bằng cách kết hợp nhiều thực thể tác tử riêng biệt thành một hệ thống đa tác tử.1 Nó cung cấp các kiểm soát chặt chẽ về cách tác tử suy nghĩ, lý luận và hợp tác.4 Việc cài đặt ADK đơn giản thông qua pip: pip install google-adk.1  
* **Agent2Agent Protocol (A2A):** Là một tiêu chuẩn mở được thiết kế để cho phép giao tiếp và hợp tác liền mạch giữa các tác tử AI, ngay cả khi chúng được xây dựng trên các framework khác nhau.2 A2A hoạt động dựa trên mô hình client-server, sử dụng JSON-RPC 2.0 qua HTTP(S) làm cơ chế giao tiếp cốt lõi.3 Điều này cho phép các tác tử ủy thác nhiệm vụ phụ, trao đổi thông tin và phối hợp hành động để giải quyết các vấn đề phức tạp mà một tác tử đơn lẻ không thể xử lý.2 A2A đảm bảo các tương tác an toàn và bảo mật, các tác tử không cần chia sẻ bộ nhớ nội bộ, công cụ hay logic độc quyền.2  
* **Model Context Protocol (MCP):** Là một tiêu chuẩn mở (ban đầu được phát triển bởi Anthropic) nhằm cung cấp một phương pháp phổ quát để kết nối các hệ thống AI với các nguồn dữ liệu và công cụ bên ngoài.7 MCP hoạt động như một "cổng USB AI", cho phép các mô hình AI tương tác với các hệ thống bên ngoài (API, cơ sở dữ liệu, tệp cục bộ) mà không cần tích hợp tùy chỉnh cho mỗi nguồn dữ liệu hoặc công cụ mới.8 MCP định nghĩa ba thành phần cơ bản: Tools (các hàm có thể thực thi), Resources (luồng dữ liệu có cấu trúc), và Prompts (mẫu hướng dẫn tái sử dụng).9 ADK hỗ trợ MCP, cho phép kết nối an toàn, hai chiều giữa nguồn dữ liệu và tác tử AI.7

Sự kết hợp của ADK, A2A và MCP tạo ra một nền tảng vững chắc, cho phép xây dựng các tác tử chuyên môn hóa cao, có khả năng giao tiếp và hợp tác hiệu quả, đồng thời dễ dàng tích hợp với các công cụ và dịch vụ bên ngoài. Điều này không chỉ giúp giải quyết các yêu cầu hiện tại mà còn tạo điều kiện cho việc mở rộng và phát triển hệ thống trong tương lai.

## **IV. Vai trò và Trách nhiệm của các Tác tử (Agent)**

Hệ thống MAS được cấu thành từ nhiều tác tử chuyên biệt, mỗi tác tử đóng một vai trò cụ thể và chịu trách nhiệm cho một tập hợp các chức năng nhất định.

### **A. Orchestrator Agent (OA)**

* **Vai trò:** Là tác tử điều phối trung tâm, "bộ não" của hệ thống.  
* **Trách nhiệm:**  
  * Tiếp nhận tất cả các yêu cầu từ người dùng hoặc hệ thống CI/CD.  
  * Phân tích yêu cầu, chia thành các nhiệm vụ con.  
  * Xác định và ủy quyền nhiệm vụ cho các tác tử chuyên biệt phù hợp thông qua giao thức A2A.  
  * Theo dõi tiến độ thực hiện nhiệm vụ của các tác tử con.  
  * Tổng hợp kết quả từ các tác tử con.  
  * Định dạng và trả kết quả cuối cùng cho người yêu cầu.  
  * Quản lý luồng công việc chung của hệ thống.  
* **Công cụ/Công nghệ chính:** ADK, A2A (client và server role tùy ngữ cảnh), có thể tích hợp LangGraph để quản lý các luồng phức tạp và trạng thái.7

### **B. Code Retrieval Agent (CRA)**

* **Vai trò:** Chuyên trách việc truy xuất mã nguồn.  
* **Trách nhiệm:**  
  * Kết nối với các kho chứa mã nguồn (ví dụ: GitHub, GitLab) hoặc truy cập hệ thống tệp cục bộ.  
  * Tải về (clone/pull) toàn bộ mã nguồn của một dự án.  
  * Truy xuất các tệp cụ thể hoặc các thay đổi (diff) liên quan đến một Pull Request.  
  * Cung cấp đường dẫn đến mã nguồn đã truy xuất hoặc nội dung mã dưới dạng MCP Resource hoặc dữ liệu trong phản hồi A2A cho các tác tử khác.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrappers cho Git CLI, GitHub API.

### **C. Static Analysis Agent (SA)**

* **Vai trò:** Thực hiện phân tích tĩnh mã nguồn để phát hiện lỗi và vấn đề.  
* **Trách nhiệm:**  
  * Thực thi các công cụ SAST (Static Application Security Testing) như Semgrep, PMD để quét mã nguồn.  
  * Phát hiện các lỗ hổng bảo mật (ví dụ: SQL injection, XSS), lỗi lập trình (ví dụ: null pointer exceptions, resource leaks), các vấn đề về coding style, và các dấu hiệu của "code smell".  
  * Phân tích các vấn đề liên quan đến kiến trúc, ví dụ như các phụ thuộc vòng, các module quá lớn, vi phạm các nguyên tắc SOLID.  
  * Trả về kết quả phân tích (thường ở định dạng JSON hoặc XML) cho OA.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrappers cho PMD, Semgrep, và các công cụ SAST khác.

### **D. Software Composition Analysis Agent (SCAA)**

* **Vai trò:** Phân tích các thành phần và thư viện phụ thuộc của dự án.  
* **Trách nhiệm:**  
  * Thực thi các công cụ SCA như OWASP Dependency-Check.  
  * Xác định danh sách các thư viện mã nguồn mở và bên thứ ba được sử dụng trong dự án.  
  * Kiểm tra các thư viện này dựa trên cơ sở dữ liệu lỗ hổng đã biết (ví dụ: NVD) để phát hiện các vấn đề bảo mật.11  
  * Kiểm tra các vấn đề về giấy phép bản quyền của thư viện.  
  * Tạo ra Software Bill of Materials (SBOM).13  
  * Trả về báo cáo lỗ hổng và thông tin giấy phép cho OA.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrappers cho OWASP Dependency-Check.

### **E. PR Review & Impact Analysis Agent (PRIA)**

* **Vai trò:** Chuyên trách review Pull Request và phân tích tác động của thay đổi.  
* **Trách nhiệm:**  
  * Phân tích các tệp đã thay đổi trong một PR.  
  * Chạy các công cụ SAST/SCA trên phạm vi các thay đổi đó.  
  * Xây dựng đồ thị cuộc gọi (call graph) hoặc đồ thị phụ thuộc (dependency graph) cho các phần mã nguồn bị ảnh hưởng.1  
  * Dựa trên phân tích đồ thị, xác định các module, lớp, hàm khác có thể bị ảnh hưởng bởi thay đổi trong PR, từ đó đề xuất các khu vực cần kiểm thử lại.  
  * Tổng hợp các lỗi mới phát hiện và danh sách các khu vực bị ảnh hưởng, gửi cho OA.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrappers cho các công cụ tạo call graph (ví dụ: python-call-graph cho Python, javaDependenceGraph cho Java), công cụ diff.

### **F. Diagram Generation Agent (DGA)**

* **Vai trò:** Tạo các sơ đồ trực quan hóa mã nguồn.  
* **Trách nhiệm:**  
  * Nhận yêu cầu tạo sơ đồ (ví dụ: sequence diagram, class diagram) từ OA, kèm theo thông tin về các lớp/hàm cần phân tích.  
  * Sử dụng các công cụ phân tích mã nguồn để trích xuất thông tin cấu trúc cần thiết.  
  * Sử dụng các công cụ tạo sơ đồ như PlantUML (thông qua text-based syntax) hoặc các thư viện chuyên dụng để tạo ra sơ đồ.16  
  * Công cụ AppMap có thể được sử dụng để tạo sequence diagram từ hành vi runtime của mã.18  
  * Trả về sơ đồ dưới dạng hình ảnh hoặc mã nguồn (ví dụ: PlantUML text) cho OA.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrappers cho PlantUML, plantuml-generator 19, AppMap, các thư viện phân tích mã để thu thập dữ liệu cho sơ đồ.

### **G. Code Suggestion Agent (CSA)**

* **Vai trò:** Đưa ra các gợi ý cải thiện mã nguồn dựa trên LLM.  
* **Trách nhiệm:**  
  * Nhận thông tin về các đoạn mã có vấn đề (ví dụ: lỗi SAST, code smell) từ OA.  
  * Sử dụng LLM (ví dụ: Gemini) để phân tích ngữ cảnh của vấn đề.  
  * Sinh ra các đoạn mã gợi ý sửa lỗi hoặc cải thiện cấu trúc, hiệu năng.  
  * Cung cấp giải thích cho các gợi ý.  
  * Trả về các gợi ý và giải thích cho OA.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrapper cho LLM API (ví dụ: Vertex AI Gemini API 1).

### **H. Q\&A Agent (QAA)**

* **Vai trò:** Tương tác hỏi đáp với người dùng về cơ sở mã.  
* **Trách nhiệm:**  
  * Tiếp nhận câu hỏi từ người dùng (thông qua OA) về các khía cạnh của mã nguồn (ví dụ: "Chức năng X hoạt động như thế nào?", "Lớp Y có trách nhiệm gì?").  
  * Sử dụng LLM kết hợp với kỹ thuật Retrieval Augmented Generation (RAG) để truy xuất thông tin liên quan từ cơ sở mã (đã được index) và tài liệu.21  
  * Có thể yêu cầu DGA tạo sơ đồ để minh họa cho câu trả lời.  
  * Sinh ra câu trả lời bằng ngôn ngữ tự nhiên, dễ hiểu.  
  * Trả về câu trả lời cho OA.  
* **Công cụ/Công nghệ chính:** ADK, A2A (server role), MCP Tool wrapper cho LLM API, MCP Tool wrapper cho hệ thống RAG (bao gồm vector database và logic truy xuất).

Sự phân chia vai trò rõ ràng này cho phép mỗi tác tử tập trung vào một lĩnh vực chuyên môn, đồng thời đảm bảo khả năng phối hợp linh hoạt để giải quyết các yêu cầu đa dạng của người dùng. Việc sử dụng ADK cho phép phát triển các tác tử này một cách module và có kiểm soát.4

## **V. Lựa chọn Công cụ Mã Nguồn Mở**

Việc lựa chọn các công cụ mã nguồn mở phù hợp là yếu tố then chốt để đảm bảo hiệu quả và tính linh hoạt của hệ thống. Dưới đây là các đề xuất công cụ cho từng hạng mục phân tích, dựa trên các yêu cầu và thông tin thu thập được.

### **A. Phân tích Tĩnh Mã nguồn (SAST)**

Các công cụ SAST quét mã nguồn mà không cần thực thi để tìm kiếm các mẫu mã độc hại, lỗ hổng bảo mật và các lỗi lập trình phổ biến.

1. **PMD:**  
   * **Mô tả:** Là một công cụ phân tích mã tĩnh đa ngôn ngữ, hỗ trợ hơn 15 ngôn ngữ.23 PMD có khả năng phát hiện các lỗi phổ biến như biến không sử dụng, khối catch trống, tạo đối tượng không cần thiết, mã trùng lặp (copy-paste detector).23  
   * **Ưu điểm:** Hỗ trợ nhiều ngôn ngữ, có hơn 400 quy tắc sẵn có và cho phép tùy chỉnh quy tắc. Tích hợp tốt với các công cụ xây dựng như Maven, Ant, Gradle.23 PMD tập trung vào mã nguồn (source code).24  
   * **Ngôn ngữ hỗ trợ (ví dụ):** Java, JavaScript, Apex, PLSQL, Python, C++, C\#.  
   * **Đầu ra:** XML, HTML, text, CSV, JSON.  
2. **Semgrep:**  
   * **Mô tả:** Một công cụ phân tích tĩnh nhanh, linh hoạt, dựa trên rule. Semgrep cho phép viết các rule tùy chỉnh dễ dàng, với cú pháp rule tương tự như mã nguồn đang phân tích.26  
   * **Ưu điểm:** Tốc độ quét nhanh (20K-100K loc/giây/rule), hỗ trợ autofix do người dùng định nghĩa, dễ dàng viết rule tùy chỉnh.26 Phù hợp cho việc quét nhanh và tích hợp vào IDE hoặc pipeline CI/CD nhẹ.27  
   * **Ngôn ngữ hỗ trợ (ví dụ):** Python, Java, JavaScript, Go, Ruby, C\#, PHP, OCaml, JSON, TypeScript.  
   * **Đầu ra:** JSON, SARIF, text, GitLab SAST/Secrets, JUnit XML.28  
   * **Lưu ý:** So với SonarQube, Semgrep mạnh về tùy chỉnh rule và tốc độ, trong khi SonarQube Community Edition cung cấp một nền tảng quản lý chất lượng mã toàn diện hơn.26  
3. **Bandit (cho Python):**  
   * **Mô tả:** Công cụ phân tích mã Python để tìm các vấn đề bảo mật phổ biến như mật khẩu hardcode, SQL injection, sử dụng hàm không an toàn.23  
   * **Ưu điểm:** Chuyên biệt cho Python, tạo báo cáo chi tiết, cho phép bỏ qua các lỗ hổng đã biết để tránh "alert fatigue".23  
   * **Đầu ra:** HTML, JSON, XML, CSV.  
4. **SpotBugs (cho Java):**  
   * **Mô tả:** Là một fork của FindBugs, phân tích bytecode Java đã biên dịch để tìm các mẫu lỗi tiềm ẩn, anti-pattern, mã không an toàn.24  
   * **Ưu điểm:** Tập trung vào mã đã biên dịch, phát hiện hơn 400 mẫu lỗi đã biết.25  
   * **Đầu ra:** XML (có thể xem bằng GUI của SpotBugs), HTML.

### **B. Phân tích Thành phần Phần mềm (SCA)**

Công cụ SCA tự động hóa việc phát hiện các lỗ hổng, vấn đề giấy phép và chất lượng tiềm ẩn trong các thành phần mã nguồn mở được sử dụng trong dự án.13

1. **OWASP Dependency-Check:**  
   * **Mô tả:** Công cụ SCA cố gắng phát hiện các lỗ hổng đã được công bố công khai trong các dependency của dự án.11 Nó xác định Common Platform Enumeration (CPE) cho dependency và liên kết với các CVE tương ứng.11  
   * **Ưu điểm:** Hỗ trợ nhiều ngôn ngữ (Java,.NET được hỗ trợ đầy đủ; Ruby, Node.js, Python ở dạng thử nghiệm 12). Có thể tích hợp qua CLI, Maven plugin, Ant task, Jenkins plugin.11 Tự động cập nhật từ NVD Data Feeds.11  
   * **Ngôn ngữ hỗ trợ (ví dụ):** Java,.NET, Python, Ruby, Node.js, C/C++.  
   * **Đầu ra:** HTML, XML, JSON, CSV.12  
   * **Lưu ý:** Mặc dù mạnh mẽ và miễn phí, nhưng có thể có tỷ lệ false positive/negative cao hơn so với các giải pháp thương mại như Snyk nếu chỉ dựa vào GAV (groupId, artifactId, version) thay vì SHA-1 của tệp.12 Snyk cung cấp cách tiếp cận chủ động hơn với việc quét thời gian thực và đề xuất sửa lỗi tự động.30

### **C. Phân tích Kiến trúc và Phụ thuộc**

Các công cụ này giúp hiểu rõ hơn về cấu trúc tổng thể và các mối quan hệ phụ thuộc trong mã nguồn.

1. **PMD (Copy-Paste Detector):** Như đã đề cập ở mục SAST, PMD có tính năng phát hiện mã trùng lặp, một yếu tố quan trọng trong việc đánh giá và cải thiện kiến trúc.23  
2. **Slizaa (cho Java):**  
   * **Mô tả:** Một workbench mã nguồn mở cho phân tích phụ thuộc phần mềm Java. Slizaa quét ứng dụng Java, lưu trữ thông tin cấu trúc trong một backend graph database (hỗ trợ Neo4j) và cho phép khám phá tương tác thông qua Cypher query, dependency structure matrix, graph view.31  
   * **Ưu điểm:** Cung cấp các công cụ trực quan hóa và truy vấn mạnh mẽ để hiểu cấu trúc phụ thuộc ở các cấp độ khác nhau (subsystem, package, file).31  
   * **Đầu ra:** Trực quan hóa trong workbench, dữ liệu có thể truy vấn bằng Cypher.  
3. **python-call-graph (cho Python):**  
   * **Mô tả:** Thư viện và công cụ dòng lệnh tạo trực quan hóa đồ thị cuộc gọi (call graph) cho ứng dụng Python.32  
   * **Ưu điểm:** Hỗ trợ Python 3.8-3.13, có thể tùy chỉnh màu sắc, nhóm module, dễ mở rộng định dạng đầu ra. Có thể sử dụng từ CLI hoặc import vào mã Python.32  
   * **Đầu ra:** Hình ảnh (ví dụ: PNG thông qua Graphviz), Gephi.  
4. **javaDependenceGraph (cho Java):**  
   * **Mô tả:** Công cụ tạo Program Dependence Graph (PDG) cho tệp đầu vào Java, có thể xuất ra tệp.dot.33 PDG bao gồm cả Control Flow edges và Data Dependency edges.33  
   * **Ưu điểm:** Giúp hiểu rõ sự tương tác giữa các biến, phương thức, lớp thông qua PDG. Có GUI để phân tích và báo cáo lỗi cú pháp/ngữ nghĩa.33  
   * **Đầu ra:** Tệp.dot (có thể trực quan hóa bằng Graphviz).

### **D. Tạo Sơ đồ từ Mã nguồn**

Các công cụ này giúp chuyển đổi mã nguồn hoặc thông tin cấu trúc thành các sơ đồ UML hoặc các dạng trực quan hóa khác.

1. **PlantUML:**  
   * **Mô tả:** Công cụ cho phép tạo sơ đồ UML (sequence, class, use case, activity, deployment) và các sơ đồ khác (ER, Gantt) từ một ngôn ngữ mô tả dựa trên văn bản đơn giản.16  
   * **Ưu điểm:** Cú pháp đơn giản, dễ tích hợp vào tài liệu (Markdown, wiki), dễ quản lý phiên bản. Hỗ trợ nhiều engine render (bao gồm Graphviz) và nhiều định dạng đầu ra (PNG, SVG, LaTeX, ASCII art).16  
   * **Kết hợp với plantuml-generator (cho Java):** plantuml-generator là một ứng dụng jar tự động tạo class diagram PlantUML từ mã nguồn Java.19 Nó quét mã nguồn Java và xuất ra cú pháp PlantUML.17  
   * **Kết hợp với goplantuml (cho Go):** Công cụ tạo class diagram PlantUML từ mã nguồn Go.35  
2. **AppMap:**  
   * **Mô tả:** Công cụ phân tích mã nguồn runtime miễn phí và mã nguồn mở, có khả năng ghi lại hành vi của mã khi chạy (ví dụ: qua test case hoặc tương tác API) để tạo sequence diagram.18  
   * **Ưu điểm:** Tạo sequence diagram tự động dựa trên hành vi thực tế của mã, giúp giữ cho sơ đồ luôn cập nhật. Hỗ trợ Ruby, Python, Java, JavaScript. Tích hợp với VSCode.18  
   * **Đầu ra:** Dữ liệu AppMap (JSON), PlantUML text, SVG.  
3. **Graphviz:**  
   * **Mô tả:** Phần mềm trực quan hóa đồ thị, sử dụng ngôn ngữ DOT để mô tả đồ thị.16 Nhiều công cụ khác sử dụng Graphviz làm engine render.16  
   * **Ưu điểm:** Ngôn ngữ DOT mạnh mẽ, hỗ trợ nhiều thuật toán layout, nhiều định dạng đầu ra (PNG, SVG, PDF, JSON).16  
   * **Sử dụng:** Các công cụ như python-call-graph và javaDependenceGraph có thể xuất ra định dạng DOT, sau đó Graphviz được dùng để render thành hình ảnh.

### **E. Bảng Tổng hợp Công cụ Đề xuất**

| Chức năng Chính | Công cụ Đề xuất | Ngôn ngữ Chính Hỗ trợ | Đầu ra Chính | Lý do Lựa chọn |
| :---- | :---- | :---- | :---- | :---- |
| **SAST (Security & Architecture)** | PMD | Đa ngôn ngữ (Java, JS, Python, etc.) | XML, JSON, HTML | Phát hiện lỗi đa dạng, quy tắc tùy chỉnh, tích hợp build tools, copy-paste detection.23 |
|  | Semgrep | Đa ngôn ngữ (Python, Java, Go, JS, etc.) | JSON, SARIF | Tốc độ cao, rule tùy chỉnh dễ dàng, phù hợp CI/CD.26 |
|  | Bandit | Python | JSON, HTML | Chuyên cho Python, tập trung vào bảo mật.23 |
|  | SpotBugs | Java (bytecode) | XML, HTML (qua GUI) | Phân tích bytecode, kế thừa FindBugs.24 |
| **SCA (Phân tích Thành phần Phần mềm)** | OWASP Dependency-Check | Đa ngôn ngữ (Java,.NET, Python, etc.) | JSON, XML, HTML | Mã nguồn mở, cộng đồng lớn, tích hợp đa dạng, tự động cập nhật NVD.11 |
| **Phân tích Kiến trúc & Phụ thuộc (Call Graph)** | python-call-graph | Python | DOT (cho Graphviz), PNG | Tạo call graph cho Python, tùy chỉnh linh hoạt.32 |
|  | javaDependenceGraph | Java | DOT (cho Graphviz) | Tạo Program Dependence Graph cho Java.33 |
|  | Slizaa | Java | Trực quan hóa trong workbench, Cypher query | Phân tích phụ thuộc sâu cho Java với graph database.31 |
| **Tạo Sơ đồ (Class, Sequence)** | PlantUML (+ plantuml-generator cho Java, goplantuml cho Go) | Đa ngôn ngữ (qua text) | PNG, SVG, text | Ngôn ngữ mô tả mạnh mẽ, dễ tích hợp, nhiều loại sơ đồ.16 |
|  | AppMap | Java, Python, Ruby, JS | PlantUML text, SVG, JSON | Tạo sequence diagram từ runtime behavior, giữ sơ đồ cập nhật.18 |
|  | Graphviz | DOT language | PNG, SVG, PDF | Engine render đồ thị mạnh mẽ, được nhiều công cụ sử dụng làm backend.16 |

Việc lựa chọn này ưu tiên các công cụ mã nguồn mở, có cộng đồng hỗ trợ mạnh mẽ và khả năng xuất kết quả ở các định dạng có cấu trúc (JSON, XML) để dễ dàng tích hợp vào hệ thống MAS. Các tác tử sẽ sử dụng các công cụ này thông qua các MCP Tool wrapper, đảm bảo tính nhất quán và khả năng thay thế khi cần.

## **VI. Giao thức Tích hợp và Giao tiếp**

Để các tác tử và công cụ trong hệ thống có thể hoạt động một cách hài hòa, việc sử dụng các giao thức chuẩn hóa cho tích hợp và giao tiếp là vô cùng quan trọng. Hệ thống này sẽ dựa trên bộ ba công nghệ của Google: ADK, MCP và A2A.

### **A. Google Agent Development Kit (ADK) để Phát triển Tác tử**

ADK là một framework mã nguồn mở được thiết kế để đơn giản hóa quá trình xây dựng các hệ thống đa tác tử phức tạp, đồng thời duy trì quyền kiểm soát chính xác đối với hành vi của tác tử.4

* **Phát triển Module:** ADK cho phép xây dựng các tác tử riêng biệt, mỗi tác tử có thể chuyên môn hóa vào một nhiệm vụ cụ thể. Điều này giúp tăng tính module, khả năng tái sử dụng và bảo trì của hệ thống.1  
* **Kiểm soát Hành vi:** ADK cung cấp các "guardrails" (rào chắn) và cơ chế điều phối (orchestration controls) để định hình cách tác tử suy nghĩ, lý luận và hợp tác.1 Điều này quan trọng để đảm bảo các tác tử hoạt động theo đúng mục tiêu và tuân thủ các quy tắc đã định.  
* **Định nghĩa Công cụ (Tools):** Trong ADK, một công cụ (tool) đơn giản là một hàm Python mà tác tử có thể gọi.20 Tác tử LLM sẽ xác định các tham số cần thiết để chạy công cụ một cách chính xác.  
* **Thiết lập:** Việc cài đặt ADK được thực hiện thông qua pip: pip install google-adk.5 Cần thiết lập môi trường ảo và các biến môi trường, ví dụ như GOOGLE\_API\_KEY nếu sử dụng các dịch vụ của Google như Gemini.5  
* **Tạo Tác tử Cơ bản:** Một tác tử cơ bản trong ADK có thể được định nghĩa với ít hơn 100 dòng mã Python, bao gồm tên, mô hình LLM sử dụng (ví dụ: gemini-1.5-flash), mô tả, chỉ dẫn (prompt) và danh sách các công cụ mà tác tử có thể sử dụng.4

ADK đóng vai trò là xương sống để xây dựng từng tác tử trong hệ thống MAS, cung cấp cấu trúc và các tiện ích cần thiết để chúng hoạt động một cách tự chủ và thông minh.

### **B. Model Context Protocol (MCP) để Kết nối Công cụ**

MCP là một tiêu chuẩn mở nhằm giải quyết vấn đề tích hợp M x N (kết nối M mô hình AI với N công cụ hoặc nguồn dữ liệu) bằng cách cung cấp một giao thức chung.8

* **"AI USB Port":** MCP hoạt động như một "cổng USB AI", cho phép tích hợp liền mạch giữa các mô hình ngôn ngữ và các hệ thống bên ngoài như API, cơ sở dữ liệu, hoặc các công cụ dòng lệnh.8  
* **Ba Thành tố Cơ bản (Primitives):** MCP tổ chức các tương tác thành ba thành tố chuẩn hóa 8:  
  1. **Tools:** Các hàm có thể thực thi mà mô hình AI có thể gọi để thực hiện hành động (ví dụ: chạy một lệnh CLI, truy vấn API).  
  2. **Resources:** Dữ liệu có cấu trúc mà mô hình có thể truy cập (ví dụ: nội dung tệp, log, phản hồi API).  
  3. **Prompts:** Các mẫu hướng dẫn có thể tái sử dụng cho các luồng công việc phổ biến, giúp định hướng tương tác với AI.  
* **Kiến trúc Client-Server:** MCP hoạt động dựa trên mô hình client-server. Host (ứng dụng AI) tương tác với Client, Client này kết nối với các MCP Server (wrapper cho các công cụ/dữ liệu).8  
* **Lợi ích:**  
  * **Tích hợp Chuẩn hóa:** Giảm thiểu sự phức tạp của việc tích hợp tùy chỉnh cho từng công cụ/nguồn dữ liệu.8  
  * **Nhận thức Ngữ cảnh Nâng cao:** Cho phép mô hình AI truy cập dữ liệu thời gian thực, cải thiện tính liên quan và cập nhật của phản hồi.8  
  * **Khám phá và Thực thi Công cụ Động:** Mô hình AI có thể truy vấn các công cụ có sẵn tại thời điểm chạy và quyết định cách sử dụng chúng.8  
  * **Bảo mật và Kiểm soát Truy cập:** MCP ưu tiên quyền riêng tư, yêu cầu sự chấp thuận rõ ràng của người dùng cho mỗi lần truy cập công cụ hoặc tài nguyên.8

Trong hệ thống này, mỗi công cụ mã nguồn mở (PMD, Semgrep, OWASP Dependency-Check, PlantUML CLI, etc.) sẽ được "bọc" (wrap) bởi một MCP Server. Các tác tử (được xây dựng bằng ADK) sẽ đóng vai trò là MCP Client, tương tác với các công cụ này thông qua giao diện MCP chuẩn hóa. Điều này giúp tách biệt logic của tác tử khỏi chi tiết triển khai của từng công cụ.

### **C. Agent2Agent Protocol (A2A) để Giao tiếp giữa các Tác tử**

A2A là một tiêu chuẩn mở do Google khởi xướng, được thiết kế để cho phép giao tiếp và khả năng tương tác giữa các hệ thống tác tử AI khác nhau.2

* **Khả năng Tương tác:** A2A cung cấp một ngôn ngữ chung, phá vỡ các rào cản và thúc đẩy khả năng tương tác giữa các tác tử được xây dựng trên các nền tảng khác nhau (ADK, LangGraph, CrewAI, v.v.).2  
* **Luồng Công việc Phức tạp:** Cho phép các tác tử ủy thác nhiệm vụ con, trao đổi thông tin và phối hợp hành động để giải quyết các vấn đề phức tạp.2  
* **An toàn và Bảo mật:** Các tác tử tương tác mà không cần chia sẻ bộ nhớ nội bộ, công cụ hoặc logic độc quyền, đảm bảo an ninh và bảo vệ tài sản trí tuệ.2 A2A được thiết kế với các tính năng xác thực, ủy quyền và quản trị tích hợp sẵn.3  
* **Cơ chế Giao tiếp:** A2A sử dụng JSON-RPC 2.0 qua HTTP(S) làm phương thức giao tiếp cốt lõi.3  
* **Các Khái niệm Chính:**  
  * **Agent Card:** Một tệp JSON hoạt động như "hồ sơ" của tác tử, mô tả khả năng, kỹ năng (skills), điểm cuối (endpoint) và các thông tin khác của tác tử.3 Các tác tử khác sử dụng Agent Card để khám phá và kết nối.  
  * **Agent Skills:** Các khả năng riêng lẻ mà một tác tử sở hữu, được liệt kê trên Agent Card của nó.3  
  * **Task Management:** Khi Tác tử A muốn Tác tử B làm điều gì đó, nó sẽ gửi một yêu cầu Task. Task là một đối tượng JSON có cấu trúc mô tả công việc cần thực hiện.3 A2A hỗ trợ các tác vụ chạy dài (long-running tasks).3  
  * **Messages:** Thông tin thực tế được trao đổi giữa các tác tử (ngữ cảnh, câu hỏi, kết quả một phần) được gửi dưới dạng tin nhắn. Tin nhắn có thể chứa nhiều phần với các loại nội dung khác nhau (văn bản, tệp, đa phương tiện).3  
* **Bổ sung cho MCP:** A2A và MCP là các tiêu chuẩn bổ sung. MCP kết nối tác tử với công cụ và tài nguyên, trong khi A2A tạo điều kiện giao tiếp động, đa phương thức giữa các tác tử khác nhau với tư cách ngang hàng.2

Trong hệ thống MAS này, Orchestrator Agent sẽ sử dụng A2A để gửi các yêu cầu Task đến các tác tử chuyên biệt (SA, SCAA, DGA, etc.). Mỗi tác tử chuyên biệt sẽ quảng bá các "skills" của mình thông qua Agent Card (ví dụ: SA Agent có skill "scan\_code\_for\_security"). Giao tiếp A2A đảm bảo rằng các tác tử có thể cộng tác một cách an toàn và hiệu quả.

### **D. Ví dụ Mã Minh họa**

Các ví dụ mã dưới đây mang tính chất minh họa khái niệm, tập trung vào cách các thành phần tương tác với nhau.

#### **1\. Định nghĩa Tác tử Cơ bản với ADK và Công cụ**

Ví dụ này minh họa cách định nghĩa một tác tử đơn giản bằng ADK, có một công cụ để tìm kiếm phim.

Python

\# file: simple\_movie\_agent/agent.py  
from google.adk.agents import Agent  
from google.adk.tools import Tool

\# Định nghĩa một công cụ (tool)  
def find\_movies\_by\_genre(genre: str, year: int \= None) \-\> str:  
    """Tìm kiếm phim dựa trên thể loại và tùy chọn năm phát hành."""  
    \# Logic giả định để tìm phim  
    movies\_db \= {  
        "sci-fi": {  
            1999:,  
            2010: \["Inception"\]  
        },  
        "action": {  
            2008:  
        }  
    }  
    results \=  
    if genre in movies\_db:  
        if year:  
            if year in movies\_db\[genre\]:  
                results.extend(movies\_db\[genre\]\[year\])  
        else:  
            for y\_movies in movies\_db\[genre\].values():  
                results.extend(y\_movies)  
      
    if not results:  
        return f"Không tìm thấy phim thể loại {genre}" \+ (f" năm {year}." if year else ".")  
    return f"Các phim tìm thấy: {', '.join(results)}"

\# Tạo đối tượng Tool từ hàm  
movie\_finder\_tool \= Tool(  
    fn=find\_movies\_by\_genre,  
    description="Một công cụ để tìm kiếm phim dựa trên thể loại và năm."  
)

\# Định nghĩa tác tử  
movie\_agent \= Agent(  
    name="MovieAgent",  
    model="gemini-1.5-flash-latest", \# Hoặc một mô hình Gemini phù hợp  
    description="Tác tử giúp tìm kiếm thông tin phim ảnh.",  
    instruction="Bạn là một trợ lý hữu ích có thể trả lời các câu hỏi về phim ảnh. Hãy sử dụng công cụ được cung cấp nếu cần.",  
    tools=\[movie\_finder\_tool\],  
)

\# Để chạy tác tử này, bạn cần thiết lập Runner của ADK  
\# from google.adk.runners import Runner  
\# if \_\_name\_\_ \== "\_\_main\_\_":  
\#     Runner(agent=movie\_agent).run()

(Dựa trên 20\)  
Trong ví dụ này, find\_movies\_by\_genre là một hàm Python đơn giản được chuyển đổi thành một Tool mà MovieAgent có thể sử dụng. Tác tử LLM sẽ tự động suy luận khi nào cần gọi công cụ này và với tham số nào dựa trên instruction và description của công cụ.

#### **2\. Wrapper Công cụ MCP cho Semgrep (Conceptual)**

Ví dụ này phác thảo cách một công cụ dòng lệnh như Semgrep có thể được bọc trong một MCP Server.

Python

\# Conceptual MCP Tool Wrapper for Semgrep  
\# Giả định có một thư viện MCP server (ví dụ: mcp\_server\_framework)

\# from mcp\_server\_framework import MCPTool, MCPResource, serve\_mcp  
import subprocess  
import json

\# @MCPTool.register(name="semgrep\_scan", description="Chạy Semgrep để quét mã nguồn.")  
async def run\_semgrep\_scan(  
    \# @MCPTool.param(description="Đường dẫn đến thư mục mã nguồn cần quét.")  
    source\_directory: str,  
    \# @MCPTool.param(description="Cấu hình rule của Semgrep (ví dụ: 'p/ci', hoặc đường dẫn tệp rule).", default="auto")  
    config: str \= "auto"  
) \-\> str: \# MCPResource (representing JSON output)  
    """  
    Thực thi Semgrep trên một thư mục mã nguồn và trả về kết quả dưới dạng JSON.  
    """  
    try:  
        \# Lệnh để chạy Semgrep và lấy output JSON  
        \# semgrep scan \--json \--output semgrep\_results.json \--config \<config\> \<source\_directory\>  
        \# Để đơn giản, ví dụ này sẽ xuất ra stdout  
        command \=  
          
        \# Thực thi lệnh  
        process \= subprocess.run(command, capture\_output=True, text=True, check=True)  
          
        \# Kết quả JSON từ stdout của Semgrep  
        \# Trong thực tế, có thể ghi vào tệp và trả về MCPResource trỏ đến tệp đó  
        return process.stdout \# Trả về chuỗi JSON  
      
    except subprocess.CalledProcessError as e:  
        \# Xử lý lỗi nếu Semgrep trả về exit code khác 0  
        error\_output \= e.stderr or e.stdout or "Lỗi không xác định từ Semgrep."  
        \# Trả về lỗi dưới dạng JSON hoặc một cấu trúc lỗi MCPResource  
        return json.dumps({"error": "Semgrep execution failed", "details": error\_output})  
    except FileNotFoundError:  
        return json.dumps({"error": "Semgrep command not found. Hãy đảm bảo Semgrep đã được cài đặt và có trong PATH."})

\# if \_\_name\_\_ \== "\_\_main\_\_":  
\#     \# Khởi tạo và chạy MCP server với công cụ này  
\#     \# serve\_mcp(tools=\[run\_semgrep\_scan\], port=8080)

(Dựa trên khái niệm MCP 8 và cách Semgrep CLI hoạt động 28\)  
Một MCP Server thực tế sẽ sử dụng một framework MCP để đăng ký run\_semgrep\_scan như một "Tool". Tác tử ADK (đóng vai trò MCP Client) sau đó có thể khám phá và gọi công cụ này. Kết quả trả về (chuỗi JSON) sẽ được tác tử xử lý tiếp.

#### **3\. Tương tác A2A: Gửi và Nhận Nhiệm vụ (Conceptual)**

Ví dụ này minh họa cách một Orchestrator Agent (Client) gửi nhiệm vụ cho một Static Analysis Agent (Server) qua A2A.

Python

\# \--- Orchestrator Agent (Client-side conceptual code) \---  
\# Giả định đã có thư viện A2AClient và các model như Task, MessagePart  
\# from a2a\_client import A2AClient, Task, MessagePart, SendMessageRequest, MessageSendParams  
\# import httpx  
\# import uuid

async def assign\_scan\_task\_to\_sa\_agent(sa\_agent\_url: str, code\_path: str):  
    \# async with httpx.AsyncClient() as http\_client:  
        \# Lấy client từ Agent Card của SA Agent  
        \# sa\_client \= await A2AClient.get\_client\_from\_agent\_card\_url(http\_client, sa\_agent\_url)  
          
        \# Tạo payload cho nhiệm vụ  
        \# task\_payload \= {  
        \#     "skill": "static\_analysis.scan\_directory", \# Tên skill của SA Agent  
        \#     "inputs": {  
        \#         "directory\_path": code\_path,  
        \#         "ruleset": "p/security-code-scan" \# Ví dụ ruleset  
        \#     }  
        \# }  
        \# Hoặc sử dụng message/send nếu SA Agent hỗ trợ  
        \# message\_payload \= {  
        \#     'message': {  
        \#         'role': 'user', \# OA là user đối với SA Agent  
        \#         'parts': \[  
        \#             {'type': 'text', 'text': f"Hãy quét thư mục {code\_path} với ruleset security-code-scan."}  
        \#             \# Có thể thêm part kiểu 'application/json' để truyền tham số có cấu trúc  
        \#         \],  
        \#         'messageId': uuid.uuid4().hex,  
        \#     },  
        \# }  
        \# request \= SendMessageRequest(params=MessageSendParams(\*\*message\_payload))  
          
        \# print(f"Gửi yêu cầu quét đến SA Agent cho đường dẫn: {code\_path}")  
        \# response \= await sa\_client.send\_message(request) \# Hoặc một phương thức gửi task tương ứng  
          
        \# Xử lý phản hồi từ SA Agent  
        \# if response and response.result:  
        \#     print("Nhận được kết quả từ SA Agent:")  
        \#     \# Giả sử kết quả là một message chứa JSON  
        \#     for part in response.result.parts:  
        \#         if part.type \== 'text' or part.type \== 'application/json':  
        \#             print(part.text) \# Hoặc part.json nếu có  
        \# else:  
        \#     print("Không nhận được phản hồi hợp lệ từ SA Agent.")  
    pass \# Mã giả

\# \--- Static Analysis Agent (Server-side conceptual request handler for A2A) \---  
\# Giả định có framework A2A server và cách đăng ký handler cho skill  
\# from a2a\_server\_framework import register\_skill\_handler, A2AResponse  
\# from some\_mcp\_tool\_library import semgrep\_mcp\_tool \# MCP tool đã được wrapper

\# @register\_skill\_handler("static\_analysis.scan\_directory")  
async def handle\_scan\_directory\_request(inputs: dict) \-\> dict: \# A2AResponse (conceptual)  
    """  
    Xử lý yêu cầu quét thư mục từ Orchestrator Agent.  
    """  
    \# directory\_path \= inputs.get("directory\_path")  
    \# ruleset \= inputs.get("ruleset", "auto")  
      
    \# if not directory\_path:  
    \#     return {"error": "Thiếu thông tin directory\_path"} \# A2AResponse.error(...)

    \# print(f"SA Agent nhận được yêu cầu quét: {directory\_path} với ruleset {ruleset}")  
      
    \# Gọi MCP tool để thực thi Semgrep  
    \# semgrep\_results\_json\_str \= await semgrep\_mcp\_tool.run\_semgrep\_scan(  
    \#     source\_directory=directory\_path,  
    \#     config=ruleset  
    \# )  
      
    \# Chuẩn bị phản hồi A2A  
    \# response\_parts \= \[{'type': 'application/json', 'text': semgrep\_results\_json\_str}\]  
    \# return {"status": "success", "outputs": {"scan\_results\_json": semgrep\_results\_json\_str}} \# A2AResponse.success(...)  
    pass \# Mã giả

(Dựa trên khái niệm A2A 2\)  
Ví dụ này cho thấy OA (client) gửi một yêu cầu (task hoặc message) đến SA Agent (server) để thực hiện một "skill" là static\_analysis.scan\_directory. SA Agent sau đó sẽ sử dụng MCP tool (như trong ví dụ 2\) để chạy Semgrep và trả kết quả về cho OA. A2A protocol sẽ định nghĩa cấu trúc chính xác của các request và response này.

#### **4\. Thực thi Công cụ CLI và Xử lý Kết quả JSON (Conceptual)**

Đây là một phần của logic bên trong một MCP Tool wrapper, tương tự như ví dụ 2, nhưng tập trung vào việc thực thi CLI và parse JSON.

Python

import subprocess  
import json

def execute\_cli\_tool\_and\_get\_json(command\_args: list) \-\> dict:  
    """  
    Thực thi một công cụ dòng lệnh và parse output JSON của nó.  
    \`command\_args\` là một list các argument, ví dụ: \["semgrep", "scan", "--json", "my\_code\_dir"\]  
    """  
    try:  
        process \= subprocess.run(  
            command\_args,  
            capture\_output=True,  \# Thu giữ stdout và stderr  
            text=True,            \# Giải mã output dưới dạng text (UTF-8 mặc định)  
            check=True            \# Ném CalledProcessError nếu exit code khác 0  
        )  
          
        \# Parse JSON từ stdout  
        \# Một số công cụ có thể ghi JSON vào một tệp, cần điều chỉnh logic đọc tệp  
        results \= json.loads(process.stdout)  
        return results  
          
    except subprocess.CalledProcessError as e:  
        \# Lỗi khi thực thi công cụ  
        print(f"Lỗi khi chạy lệnh: {' '.join(command\_args)}")  
        print(f"Exit code: {e.returncode}")  
        print(f"Stdout: {e.stdout}")  
        print(f"Stderr: {e.stderr}")  
        return {"error": "Tool execution failed", "details": e.stderr or e.stdout}  
    except json.JSONDecodeError as e:  
        \# Lỗi khi parse JSON  
        print(f"Lỗi khi parse JSON output từ lệnh: {' '.join(command\_args)}")  
        print(f"JSONDecodeError: {e}")  
        \# process.stdout có thể chứa output không phải JSON gây lỗi  
        return {"error": "JSON decoding failed", "raw\_output": process.stdout if 'process' in locals() else "N/A"}  
    except FileNotFoundError:  
        \# Lỗi không tìm thấy công cụ (ví dụ: semgrep chưa cài)  
        print(f"Lỗi: Không tìm thấy lệnh '{command\_args}'. Hãy đảm bảo nó đã được cài đặt và có trong PATH.")  
        return {"error": f"Command not found: {command\_args}"}

\# Ví dụ sử dụng:  
\# semgrep\_results \= execute\_cli\_tool\_and\_get\_json(  
\#     \["semgrep", "scan", "--config", "auto", "--json", "./path\_to\_your\_code"\]  
\# )  
\# if "error" not in semgrep\_results:  
\#     print(f"Tìm thấy {len(semgrep\_results.get('results',))} vấn đề.")  
\# else:  
\#     print(f"Có lỗi xảy ra: {semgrep\_results\['error'\]}")

(Dựa trên cách Semgrep CLI xuất JSON 28 và các kỹ thuật Python chuẩn)  
Logic này là cốt lõi của nhiều MCP Tool wrapper. Nó cho thấy cách gọi một tiến trình con, thu thập output, và xử lý các lỗi tiềm ẩn. Kết quả JSON sau đó có thể được truyền lại cho tác tử ADK.

#### **5\. Tạo Sơ đồ (Call Graph, Class Diagram) bằng Công cụ (Conceptual)**

* **Tạo Call Graph cho Python bằng python-call-graph (trong MCP Tool):**  
  Python  
  \# Conceptual MCP Tool wrapper for python-call-graph  
  \# from pycallgraph import PyCallGraph, Config  
  \# from pycallgraph.output import GraphvizOutput  
  import os

  \# @MCPTool.register(name="generate\_python\_call\_graph",...)  
  async def generate\_python\_call\_graph(  
      \# @MCPTool.param(description="Đường dẫn đến tệp Python chính để chạy và phân tích.")  
      python\_script\_path: str,  
      \# @MCPTool.param(description="Đường dẫn tệp PNG output cho call graph.", default="callgraph.png")  
      output\_image\_path: str \= "callgraph.png"  
  ) \-\> str: \# MCPResource (path to image) or status  
      """  
      Chạy một kịch bản Python và tạo call graph bằng python-call-graph.  
      LƯU Ý QUAN TRỌNG: Việc này liên quan đến việc THỰC THI mã tùy ý (\`python\_script\_path\`).  
      Cần có các biện pháp bảo mật nghiêm ngặt trong môi trường thực tế.  
      """  
      \# if not os.path.exists(python\_script\_path):  
      \#     return json.dumps({"error": f"Script not found: {python\_script\_path}"})

      \# try:  
      \#     \# Cấu hình Graphviz output  
      \#     graphviz \= GraphvizOutput(output\_file=output\_image\_path)  
      \#     config \= Config(max\_depth=5) \# Giới hạn độ sâu để tránh đồ thị quá lớn

      \#     \# Sử dụng PyCallGraph để profile việc thực thi script  
      \#     \# CẢNH BÁO: Đoạn này thực thi mã từ python\_script\_path  
      \#     \# Đây là một rủi ro bảo mật lớn nếu script không đáng tin cậy.  
      \#     \# Trong một hệ thống sản xuất, cần có sandboxing hoặc các cơ chế an toàn khác.  
      \#     with PyCallGraph(output=graphviz, config=config):  
      \#         \# Cách đơn giản nhất là thực thi script như một module  
      \#         \# Tuy nhiên, điều này có thể phức tạp về quản lý context và dependencies  
      \#         \# Một cách tiếp cận khác là sử dụng thư viện \`ast\` để phân tích tĩnh  
      \#         \# hoặc các công cụ phân tích tĩnh call graph khác không cần thực thi.  
      \#         \# Ví dụ này chỉ minh họa cách thư viện pycallgraph được dùng theo tài liệu của nó.  
      \#         \# subprocess.run(\["python", python\_script\_path\], check=True) \# Không trực tiếp profile theo cách này

      \#         \# Cách đúng hơn là import và gọi một hàm cụ thể nếu biết trước  
      \#         \# Hoặc sử dụng CLI của pycallgraph nếu phù hợp hơn cho MCP tool  
      \#         \# pycallgraph graphviz \--./mypythonscript.py  
      \#         \# command \= \["pycallgraph", "graphviz", "--output-file", output\_image\_path, "--", python\_script\_path\]  
      \#         \# subprocess.run(command, check=True)

      \#     \# return json.dumps({"status": "success", "image\_path": output\_image\_path})  
      \# except Exception as e:  
      \#     return json.dumps({"error": f"Failed to generate call graph: {str(e)}"})  
      pass \# Mã giả

  (Dựa trên 32\)  
  Ví dụ này cho thấy cách python-call-graph có thể được gọi để tạo một tệp hình ảnh. Lưu ý quan trọng về bảo mật khi thực thi mã không đáng tin cậy. Trong thực tế, việc phân tích tĩnh để tạo call graph (nếu công cụ hỗ trợ) sẽ an toàn hơn là phân tích runtime cho mã không xác định.  
* **Tạo Class Diagram bằng PlantUML (trong MCP Tool):**  
  Python  
  \# Conceptual MCP Tool wrapper for PlantUML (using plantuml-generator for Java)  
  import subprocess  
  import os

  \# @MCPTool.register(name="generate\_java\_class\_diagram\_plantuml",...)  
  async def generate\_java\_class\_diagram(  
      \# @MCPTool.param(description="Đường dẫn đến thư mục gốc của dự án Java hoặc package cụ thể.")  
      project\_or\_package\_path: str,  
      \# @MCPTool.param(description="Đường dẫn tệp output.puml (PlantUML text).")  
      output\_puml\_path: str,  
      \# @MCPTool.param(description="Đường dẫn đến plantuml-generator.jar.")  
      generator\_jar\_path: str,  
      \# @MCPTool.param(description="Tùy chọn: Tên lớp cụ thể để tạo sơ đồ.", default=None)  
      target\_class\_name: str \= None  
  ) \-\> str: \# MCPResource (path to.puml file) or status  
      """  
      Sử dụng plantuml-generator.jar để tạo class diagram PlantUML từ mã nguồn Java.  
      """  
      \# if not os.path.exists(project\_or\_package\_path):  
      \#     return json.dumps({"error": f"Project/Package path not found: {project\_or\_package\_path}"})  
      \# if not os.path.exists(generator\_jar\_path):  
      \#     return json.dumps({"error": f"PlantUML Generator JAR not found: {generator\_jar\_path}"})

      \# command \= \[  
      \#     "java", "-jar", generator\_jar\_path,  
      \#     project\_or\_package\_path,  
      \#     output\_puml\_path  
      \# \]  
      \# if target\_class\_name:  
      \#     command.append(target\_class\_name)

      \# try:  
      \#     subprocess.run(command, check=True, capture\_output=True, text=True)  
      \#     \# Sau khi có file.puml, có thể tùy chọn render thành PNG bằng PlantUML.jar  
      \#     \# subprocess.run(\["java", "-jar", "plantuml.jar", output\_puml\_path\], check=True)  
      \#     return json.dumps({"status": "success", "puml\_file\_path": output\_puml\_path})  
      \# except subprocess.CalledProcessError as e:  
      \#     return json.dumps({  
      \#         "error": "PlantUML generation failed",  
      \#         "details": e.stderr or e.stdout  
      \#     })  
      pass \# Mã giả

  (Dựa trên 19 và 17\)  
  Ví dụ này cho thấy cách gọi plantuml-generator.jar từ dòng lệnh để tạo tệp văn bản PlantUML. Tệp này sau đó có thể được DGA xử lý tiếp (ví dụ, render thành hình ảnh bằng PlantUML.jar hoặc trả về dạng text).

Các ví dụ mã này minh họa cách các công nghệ ADK, MCP, A2A và các công cụ mã nguồn mở có thể được kết hợp để xây dựng các thành phần của hệ thống MAS. Việc triển khai thực tế sẽ đòi hỏi xử lý lỗi chi tiết hơn, cấu hình bảo mật và tối ưu hóa hiệu năng.

## **VII. Luồng Hoạt động Hệ thống Minh họa**

Các luồng hoạt động dưới đây mô tả cách hệ thống MAS xử lý các yêu cầu điển hình, thể hiện sự phối hợp giữa các tác tử chuyên biệt.

### **A. Luồng: Review Toàn bộ Mã nguồn (Kho GitHub)**

1. **Khởi tạo:** Người dùng (hoặc một hệ thống CI kích hoạt theo lịch) gửi yêu cầu review toàn bộ mã nguồn của một kho GitHub đến Orchestrator Agent (OA), cung cấp URL của kho.  
2. **Truy xuất Mã nguồn:** OA gửi một A2A Task đến Code Retrieval Agent (CRA) với nội dung: "Truy xuất mã nguồn từ {URL\_kho\_GitHub}".  
3. **CRA Thực thi:** CRA sử dụng MCP Tool (wrapper cho Git CLI) để clone kho mã nguồn về một vị trí tạm thời trên hệ thống tệp. Sau đó, CRA phản hồi OA qua A2A với đường dẫn đến thư mục mã nguồn đã tải về.  
4. **Phân tích SAST:** OA gửi A2A Task đến Static Analysis Agent (SA): "Thực hiện phân tích SAST cho mã nguồn tại {đường\_dẫn\_mã} sử dụng bộ quy tắc {cấu\_hình\_bảo\_mật\_và\_kiến\_trúc}".  
5. **SA Thực thi (Semgrep & PMD):**  
   * SA sử dụng MCP Tool cho Semgrep, thực thi lệnh quét với cấu hình phù hợp (ví dụ: semgrep scan \--config p/security \--json {đường\_dẫn\_mã}). Kết quả JSON được trả về cho SA.  
   * SA sử dụng MCP Tool cho PMD, thực thi lệnh quét (ví dụ: pmd \-d {đường\_dẫn\_mã} \-R rulesets/java/quickstart.xml \-f xml). Kết quả XML được trả về cho SA.  
   * SA tổng hợp kết quả từ cả hai công cụ và gửi lại cho OA qua A2A.  
6. **Phân tích SCA:** OA gửi A2A Task đến Software Composition Analysis Agent (SCAA): "Phân tích các thành phần phụ thuộc cho dự án tại {đường\_dẫn\_mã}".  
7. **SCAA Thực thi:** SCAA sử dụng MCP Tool cho OWASP Dependency-Check (ví dụ: dependency-check \--scan {đường\_dẫn\_mã} \--format JSON \--project "MyProject"). Báo cáo lỗ hổng dạng JSON được gửi lại cho OA qua A2A.  
8. **Tổng hợp và Gợi ý (Tùy chọn):**  
   * OA tổng hợp tất cả các phát hiện từ SA và SCAA.  
   * Nếu có các lỗ hổng nghiêm trọng hoặc các vấn đề kiến trúc phức tạp, OA có thể gửi một A2A Task đến Code Suggestion Agent (CSA): "Đề xuất giải pháp cho {danh\_sách\_lỗ\_hổng} trong {các\_đoạn\_mã\_liên\_quan}".  
   * CSA sử dụng LLM (thông qua MCP Tool) để phân tích và tạo ra các gợi ý sửa lỗi hoặc cải thiện mã. Các gợi ý này được gửi lại cho OA.  
9. **Hoàn tất và Báo cáo:** OA biên soạn một báo cáo tổng hợp bao gồm tất cả các phát hiện SAST, SCA và các gợi ý (nếu có). Báo cáo này được gửi lại cho người dùng hoặc hệ thống đã khởi tạo yêu cầu.

Luồng công việc này cho thấy sự phân chia trách nhiệm rõ ràng: CRA lấy mã, SA và SCAA phân tích, CSA đề xuất, và OA điều phối toàn bộ quá trình. A2A là kênh giao tiếp chính giữa các tác tử, trong khi MCP là cầu nối đến các công具 phân tích cụ thể.

### **B. Luồng: Phân tích Pull Request Tự động và Báo cáo Ảnh hưởng Phụ**

1. **Kích hoạt:** Một hệ thống CI (ví dụ: GitHub Actions) phát hiện một Pull Request (PR) mới hoặc một cập nhật cho PR hiện có. Hệ thống CI này kích hoạt OA, truyền thông tin chi tiết về PR (ví dụ: ID PR, URL kho, nhánh nguồn, nhánh đích).  
2. **Truy xuất Thay đổi PR:** OA gửi A2A Task đến CRA: "Truy xuất các tệp đã thay đổi và nội dung diff cho PR {ID\_PR} trong kho {URL\_kho}".  
3. **CRA Thực thi:** CRA sử dụng MCP Tool (wrapper cho API của nền tảng Git như GitHub API, hoặc Git CLI) để lấy danh sách các tệp đã thay đổi và nội dung diff của chúng. Thông tin này được gửi lại cho OA.  
4. **Phân tích SAST trên Thay đổi:** OA gửi A2A Task đến SA: "Quét các tệp đã thay đổi {danh\_sách\_tệp} với bộ quy tắc {cấu\_hình\_cho\_PR}". Việc chỉ quét các tệp thay đổi giúp tăng tốc độ phân tích.  
5. **SA Thực thi:** SA sử dụng MCP Tool (ví dụ: Semgrep) để quét chỉ các tệp được chỉ định. Kết quả phân tích (các vấn đề mới hoặc liên quan đến thay đổi) được gửi lại cho OA.  
6. **Phân tích Tác động:** OA gửi A2A Task đến PR Review & Impact Analysis Agent (PRIA): "Phân tích tác động của các thay đổi trong {danh\_sách\_tệp\_thay\_đổi} đối với toàn bộ dự án tại {đường\_dẫn\_mã\_gốc\_của\_nhánh\_đích}".  
7. **PRIA Thực thi:**  
   * PRIA sử dụng MCP Tool để tạo đồ thị cuộc gọi (call graph) hoặc đồ thị phụ thuộc cho các tệp đã thay đổi và các thành phần liên quan trong cơ sở mã của nhánh đích. Ví dụ, nếu dự án là Python, nó có thể dùng python-call-graph 32; nếu là Java, có thể dùng javaDependenceGraph 33 hoặc Slizaa 31 để phân tích.  
   * Dựa trên đồ thị, PRIA xác định các hàm, lớp, module khác trong hệ thống có thể bị ảnh hưởng gián tiếp bởi các thay đổi trong PR (ví dụ: các hàm gọi đến hàm đã sửa đổi, hoặc các hàm được gọi bởi hàm đã sửa đổi có hành vi thay đổi). Đây là việc xác định "blast radius" của thay đổi.15  
   * PRIA gửi lại cho OA một danh sách các vấn đề SAST mới (nếu có) và một danh sách các khu vực/tệp/hàm được đề xuất cần kiểm thử lại (impacted areas for re-testing).  
8. **Đăng Nhận xét PR:** OA tổng hợp kết quả từ SA và PRIA. Sau đó, OA có thể sử dụng một MCP Tool (wrapper cho API của nền tảng Git) để tự động đăng một nhận xét vào PR, liệt kê các vấn đề tìm thấy và các khu vực cần chú ý kiểm thử.

Luồng này nhấn mạnh khả năng của hệ thống trong việc cung cấp phản hồi nhanh chóng và tập trung cho các PR, giúp nhà phát triển sớm phát hiện lỗi và hiểu rõ hơn về phạm vi ảnh hưởng của thay đổi. Việc sử dụng đồ thị cuộc gọi/phụ thuộc là một kỹ thuật quan trọng để phân tích tác động thay đổi.14

### **C. Luồng: Hỏi đáp Tương tác về Cơ sở Mã (ví dụ: "Tạo sơ đồ sequence cho quy trình thanh toán")**

1. **Người dùng Đặt câu hỏi:** Người dùng tương tác với hệ thống (có thể qua một giao diện chat hoặc IDE plugin) và đặt câu hỏi cho Q\&A Agent (QAA), được chuyển tiếp qua OA: "Hãy tạo sơ đồ sequence mô tả quy trình xử lý thanh toán trong module 'PaymentService'".  
2. **QAA Phân tích Yêu cầu:**  
   * QAA sử dụng LLM (thông qua MCP Tool) để hiểu ý định của người dùng.  
   * Kết hợp với kỹ thuật RAG 21, QAA truy vấn một cơ sở kiến thức (knowledge base) đã được xây dựng từ mã nguồn của dự án (ví dụ: mã nguồn được phân tích và lưu trữ dưới dạng vector embeddings) để xác định các lớp, phương thức và tương tác chính liên quan đến "quy trình xử lý thanh toán" trong "PaymentService".  
3. **Yêu cầu Tạo Sơ đồ:** QAA xác định rằng cần một sơ đồ sequence để trả lời. Nó gửi một A2A Task đến Diagram Generation Agent (DGA): "Tạo sơ đồ sequence cho các tương tác liên quan đến các thành phần sau: {danh\_sách\_lớp\_và\_phương\_thức\_liên\_quan\_đến\_thanh\_toán}".  
4. **DGA Thực thi:**  
   * DGA nhận yêu cầu. Nó có thể sử dụng một MCP Tool để phân tích mã nguồn của các lớp/phương thức được chỉ định.  
   * Sau đó, DGA sử dụng một MCP Tool khác (wrapper cho PlantUML 16 hoặc AppMap 18) để tạo ra mã nguồn PlantUML cho sơ đồ sequence. Nếu sử dụng AppMap, nó có thể cần thực thi (hoặc mô phỏng thực thi) một kịch bản liên quan đến thanh toán để ghi lại các tương tác.  
   * DGA gửi lại mã PlantUML (hoặc hình ảnh sơ đồ đã render) cho QAA qua A2A.  
5. **QAA Tổng hợp và Trả lời:**  
   * QAA nhận được sơ đồ từ DGA.  
   * QAA sử dụng LLM để tạo một lời giải thích bằng ngôn ngữ tự nhiên đi kèm với sơ đồ, mô tả các bước chính trong quy trình thanh toán.  
   * QAA gửi câu trả lời hoàn chỉnh (bao gồm giải thích và sơ đồ) cho OA, sau đó OA chuyển đến người dùng.

Luồng này thể hiện khả năng tương tác thông minh của hệ thống. QAA không chỉ đơn thuần tìm kiếm từ khóa mà còn hiểu ngữ nghĩa, phối hợp với DGA để trực quan hóa thông tin, và sử dụng LLM để trình bày kết quả một cách dễ hiểu. Việc sử dụng RAG giúp LLM truy cập thông tin cập nhật và chính xác từ cơ sở mã.22

Các luồng hoạt động này cho thấy tính linh hoạt và sức mạnh của kiến trúc MAS, nơi các tác tử chuyên biệt, được xây dựng trên ADK, giao tiếp qua A2A và sử dụng các công cụ bên ngoài qua MCP, cùng nhau giải quyết các tác vụ phức tạp trong vòng đời phát triển phần mềm.

## **VIII. Các Vấn đề Nâng cao và Hướng Phát triển Tương lai**

Mặc dù kiến trúc đề xuất cung cấp một nền tảng mạnh mẽ, việc triển khai và vận hành một hệ thống MAS như vậy trong thực tế đòi hỏi phải xem xét nhiều yếu tố nâng cao và các hướng phát triển tiềm năng.

### **A. Khả năng Mở rộng và Hiệu năng**

* **Mở rộng Tác tử:** Các tác tử phân tích (SA, SCAA, PRIA, DGA) thường là các tác tử không trạng thái (stateless) hoặc có trạng thái giới hạn trong một phiên làm việc. Điều này cho phép triển khai nhiều thực thể (instance) của cùng một loại tác tử để xử lý song song nhiều yêu cầu, từ đó tăng thông lượng của hệ thống. ADK và các nền tảng triển khai như Vertex AI Agent Engine 4 có thể hỗ trợ việc này.  
* **Cơ chế Cache:** Đối với các tác vụ phân tích lặp đi lặp lại trên cùng một phiên bản mã nguồn hoặc các phần không thay đổi của mã, việc triển khai cơ chế cache cho kết quả phân tích (ví dụ: kết quả SAST, SCA, đồ thị phụ thuộc) có thể giảm đáng kể thời gian xử lý và tài nguyên tính toán.  
* **Tối ưu hóa Tương tác LLM:** Các lệnh gọi đến LLM có thể tốn kém về thời gian và chi phí. Cần áp dụng các kỹ thuật như batching (nhóm nhiều yêu cầu nhỏ thành một yêu cầu lớn), prompt engineering (thiết kế prompt hiệu quả để giảm số token và tăng độ chính xác), và lựa chọn mô hình LLM phù hợp với từng tác vụ (ví dụ: mô hình nhỏ hơn, nhanh hơn cho các tác vụ đơn giản). Gemini 1.5 Pro cung cấp context window lớn, có thể hữu ích cho việc phân tích các tài liệu dài.1  
* **Hiệu năng I/O và Mạng:** Việc truy xuất mã nguồn lớn, truyền dữ liệu kết quả phân tích giữa các tác tử và giữa tác tử với công cụ cần được tối ưu hóa. Sử dụng các định dạng dữ liệu nén, giao thức mạng hiệu quả và cân nhắc vị trí địa lý của các thành phần hệ thống là cần thiết.

### **B. Tăng cường Bảo mật**

* **Bảo mật Kênh A2A:** Giao tiếp giữa các tác tử qua A2A phải được bảo mật bằng HTTPS. Cần triển khai các cơ chế xác thực (authentication) và ủy quyền (authorization) mạnh mẽ để đảm bảo chỉ các tác tử được phép mới có thể giao tiếp và yêu cầu thực thi "skill" từ nhau.3  
* **Bảo mật Truy cập Công cụ MCP:** Việc truy cập vào các MCP Tool (đặc biệt là những công cụ thực thi lệnh CLI hoặc tương tác với hệ thống tệp) cần được kiểm soát chặt chẽ. Cần có cơ chế phân quyền chi tiết, xác thực đầu vào (input sanitization) để tránh các lỗ hổng như command injection. MCP được thiết kế với ưu tiên về quyền riêng tư, yêu cầu sự chấp thuận rõ ràng cho mỗi lần truy cập.8  
* **Quản lý Bí mật:** Các API key (cho GitHub, LLM services, NVD API 43), mật khẩu cơ sở dữ liệu và các thông tin nhạy cảm khác phải được lưu trữ và quản lý một cách an toàn, ví dụ sử dụng các dịch vụ quản lý bí mật chuyên dụng (như Google Secret Manager, HashiCorp Vault) và không bao giờ hardcode trong mã nguồn hoặc cấu hình.  
* **Chống Prompt Injection:** Nếu LLM được sử dụng để diễn giải output từ các công cụ hoặc để tạo ra các lệnh cho các công cụ khác, cần có biện pháp phòng chống prompt injection. Điều này bao gồm việc làm sạch và kiểm tra kỹ lưỡng dữ liệu đầu vào cho LLM và output từ LLM trước khi sử dụng.

### **C. Khả năng Mở rộng Chức năng**

* **Hỗ trợ Ngôn ngữ Lập trình Mới:** Để hỗ trợ một ngôn ngữ lập trình mới, cần cập nhật hoặc bổ sung:  
  * Các bộ quy tắc (rulesets) cho công cụ SAST (PMD, Semgrep).  
  * Các trình phân tích (parser) cho công cụ SCA (OWASP Dependency-Check) nếu cần.  
  * Các công cụ tạo sơ đồ và phân tích phụ thuộc tương thích với ngôn ngữ đó.  
  * Có thể cần huấn luyện lại hoặc tinh chỉnh (fine-tune) LLM nếu các tác vụ Q\&A và gợi ý mã yêu cầu hiểu biết sâu về ngôn ngữ mới.  
* **Tích hợp Công cụ Phân tích Mới:** Việc tích hợp một công cụ phân tích mới đòi hỏi phải xây dựng một MCP Tool wrapper mới cho công cụ đó. Nếu công cụ cung cấp chức năng hoàn toàn mới, có thể cần tạo ra một loại tác tử chuyên biệt mới hoặc mở rộng khả năng của một tác tử hiện có.  
* **Cập nhật Mô hình LLM:** Hệ thống nên được thiết kế để dễ dàng chuyển đổi hoặc cập nhật lên các phiên bản LLM mới hơn, mạnh mẽ hơn khi chúng ra mắt. ADK cho phép lựa chọn mô hình ưa thích.4

### **D. Giao diện Người dùng (UI) / Tích hợp IDE**

Mặc dù hệ thống có thể hoạt động hoàn toàn tự động thông qua CI/CD hoặc API, việc cung cấp giao diện người dùng thân thiện sẽ tăng cường khả năng sử dụng và tương tác:

* **Web UI:** Một giao diện web có thể cho phép người dùng khởi tạo các tác vụ review, xem báo cáo tổng hợp, quản lý cấu hình, và tương tác trực tiếp với Q\&A Agent.  
* **IDE Plugins:** Tích hợp trực tiếp vào các IDE phổ biến (VS Code, IntelliJ IDEA, PyCharm) có thể cung cấp phản hồi và gợi ý theo thời gian thực cho nhà phát triển ngay khi họ viết mã. Ví dụ, plugin có thể hiển thị các cảnh báo SAST hoặc gợi ý từ CSA. ADK hỗ trợ các khả năng streaming âm thanh và video hai chiều, mở ra tiềm năng cho các tương tác phong phú hơn.4

### **E. Quản lý Trạng thái và Các Tác vụ Chạy Dài**

Đối với các luồng công việc phức tạp và kéo dài (ví dụ: review một kho mã nguồn rất lớn), việc quản lý trạng thái một cách tin cậy là rất quan trọng.

* **LangGraph Checkpointers:** Nếu Orchestrator Agent hoặc một tác tử chuyên biệt nào đó cần quản lý một quy trình nhiều bước phức tạp, việc sử dụng LangGraph với các "checkpointer" có thể giúp lưu trữ và phục hồi trạng thái của tác tử, đảm bảo khả năng phục hồi sau gián đoạn và quản lý các tác vụ chạy dài.7 Google Cloud cung cấp các thư viện tích hợp để lưu trữ trạng thái này vào các cơ sở dữ liệu được quản lý như PostgreSQL.7  
* **A2A Long-Running Tasks:** Bản thân giao thức A2A cũng hỗ trợ các tác vụ chạy dài, cho phép các tác tử cập nhật trạng thái cho nhau ("Vẫn đang xử lý... gần xong...") trong thời gian dài nếu cần.3

### **F. Đánh giá và Độ Chính xác**

* **Độ chính xác của Phân tích:** Cần có quy trình để đánh giá và cải thiện độ chính xác của các công cụ SAST/SCA, bao gồm việc giảm thiểu tỷ lệ false positives (cảnh báo sai về lỗi không tồn tại) và false negatives (bỏ sót lỗi thực sự). Điều này có thể bao gồm việc tùy chỉnh rulesets, sử dụng nhiều công cụ và đối chiếu kết quả.  
* **Hiệu quả của Phân tích Tác động:** Đo lường mức độ hiệu quả của PRIA trong việc xác định các khu vực bị ảnh hưởng bởi PR. Phản hồi từ đội ngũ QA và kiểm thử có thể được sử dụng để tinh chỉnh thuật toán phân tích tác động.  
* **Phản hồi Người dùng:** Thu thập phản hồi từ người dùng về chất lượng của các câu trả lời từ QAA và các gợi ý từ CSA để liên tục cải thiện prompt, dữ liệu RAG và logic của các tác tử này. Vertex AI cung cấp các công cụ đánh giá và Example Store để cải thiện hiệu năng của tác tử dựa trên sử dụng thực tế.4

Việc giải quyết các vấn đề nâng cao này sẽ đảm bảo hệ thống MAS không chỉ mạnh mẽ về mặt lý thuyết mà còn hiệu quả, an toàn và dễ sử dụng trong môi trường phát triển phần mềm thực tế. Kiến trúc module dựa trên ADK, A2A và MCP tạo nền tảng tốt để giải quyết các thách thức này một cách có hệ thống.

## **IX. Kết luận**

Báo cáo này đã trình bày một thiết kế chi tiết cho hệ thống Multi-Agent (MAS) nhằm tự động hóa và nâng cao hiệu quả của quy trình review mã nguồn, phân tích Pull Request và hỗ trợ nhà phát triển thông qua tương tác hỏi đáp. Bằng cách tận dụng các công nghệ tiên tiến từ Google như Agent Development Kit (ADK), Model Context Protocol (MCP) và Agent2Agent Protocol (A2A), kết hợp với sức mạnh của các Mô hình Ngôn ngữ Lớn và một loạt các công cụ phân tích mã nguồn mở, hệ thống đề xuất hứa hẹn mang lại nhiều lợi ích đáng kể.

Kiến trúc MAS với các tác tử chuyên biệt cho phép xử lý các tác vụ phức tạp một cách module và hiệu quả. Việc sử dụng ADK cung cấp một framework vững chắc để phát triển và quản lý các tác tử này. MCP chuẩn hóa cách các tác tử tương tác với các công cụ bên ngoài, giúp dễ dàng tích hợp và mở rộng thư viện công cụ. Trong khi đó, A2A đảm bảo giao tiếp an toàn và linh hoạt giữa các tác tử, cho phép chúng cộng tác để đạt được các mục tiêu chung.

Các luồng hoạt động minh họa đã cho thấy cách hệ thống có thể xử lý các yêu cầu thực tế như review toàn bộ kho mã, phân tích PR và trả lời các câu hỏi về mã nguồn. Việc lựa chọn cẩn thận các công cụ mã nguồn mở như PMD, Semgrep, OWASP Dependency-Check, PlantUML và các công cụ phân tích đồ thị phụ thuộc đảm bảo rằng hệ thống có thể thực hiện các phân tích sâu rộng trên nhiều khía cạnh của mã nguồn.

Tuy nhiên, để triển khai thành công một hệ thống như vậy, cần chú trọng đến các yếu tố nâng cao như khả năng mở rộng, hiệu năng, bảo mật, khả năng mở rộng chức năng, giao diện người dùng và quản lý trạng thái. Việc liên tục đánh giá và cải thiện độ chính xác của các phân tích cũng là một yếu tố quan trọng để duy trì giá trị của hệ thống.

Tóm lại, hệ thống Multi-Agent được đề xuất có tiềm năng cách mạng hóa cách chúng ta tiếp cận việc đảm bảo chất lượng và bảo mật phần mềm. Với một thiết kế kiến trúc hợp lý, lựa chọn công nghệ phù hợp và sự đầu tư vào việc giải quyết các thách thức nâng cao, hệ thống này có thể trở thành một công cụ vô giá, giúp các đội ngũ phát triển xây dựng phần mềm tốt hơn, nhanh hơn và an toàn hơn.

#### **Works cited**

1. From Prototypes to Agents with ADK \- Google Codelabs, accessed June 8, 2025, [https://codelabs.developers.google.com/your-first-agent-with-adk](https://codelabs.developers.google.com/your-first-agent-with-adk)  
2. Agent2Agent Protocol (A2A) \- Google, accessed June 8, 2025, [https://google.github.io/A2A/resources/](https://google.github.io/A2A/resources/)  
3. Inside Google's Agent2Agent (A2A) Protocol: Teaching AI Agents to Talk to Each Other, accessed June 8, 2025, [https://towardsdatascience.com/inside-googles-agent2agent-a2a-protocol-teaching-ai-agents-to-talk-to-each-other/](https://towardsdatascience.com/inside-googles-agent2agent-a2a-protocol-teaching-ai-agents-to-talk-to-each-other/)  
4. Vertex AI Agent Builder | Google Cloud, accessed June 8, 2025, [https://cloud.google.com/products/agent-builder](https://cloud.google.com/products/agent-builder)  
5. Quickstart: Build an agent with the Agent Development Kit | Generative AI on Vertex AI, accessed June 8, 2025, [https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart)  
6. Building A Secure Agentic AI Application Leveraging Google's A2A Protocol \- arXiv, accessed June 8, 2025, [https://arxiv.org/pdf/2504.16902](https://arxiv.org/pdf/2504.16902)  
7. MCP Toolbox for Databases (formerly Gen AI Toolbox for Databases) now supports Model Context Protocol (MCP) | Google Cloud Blog, accessed June 8, 2025, [https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases-now-supports-model-context-protocol](https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases-now-supports-model-context-protocol)  
8. Model Context Protocol (MCP) Explained \- Humanloop, accessed June 8, 2025, [https://humanloop.com/blog/mcp](https://humanloop.com/blog/mcp)  
9. Model Context Protocol (MCP) \- The Future of AI Integration \- Digidop, accessed June 8, 2025, [https://www.digidop.com/blog/mcp-ai-revolution](https://www.digidop.com/blog/mcp-ai-revolution)  
10. What is the Model Context Protocol (MCP)? | Explained In Plain English, accessed June 8, 2025, [https://plainenglish.io/eli5/what-is-model-context-protocol](https://plainenglish.io/eli5/what-is-model-context-protocol)  
11. OWASP Dependency-Check | OWASP Foundation, accessed June 8, 2025, [https://owasp.org/www-project-dependency-check/](https://owasp.org/www-project-dependency-check/)  
12. OWASP Dependency Check: How It Works, Pros, and Cons \- Mend.io, accessed June 8, 2025, [https://www.mend.io/blog/owasp-dependency-check/](https://www.mend.io/blog/owasp-dependency-check/)  
13. SCA (Software Composition Analysis) \- FOSSA Learning Center | Interactive Guides, accessed June 8, 2025, [https://fossa.com/learn/software-composition-analysis/](https://fossa.com/learn/software-composition-analysis/)  
14. Enhancing Code Analysis With Code Graphs \- DZone, accessed June 8, 2025, [https://dzone.com/articles/enhancing-code-analysis-with-code-graphs](https://dzone.com/articles/enhancing-code-analysis-with-code-graphs)  
15. Understanding Software Dependency Graphs | Blog \- VulnCheck, accessed June 8, 2025, [https://vulncheck.com/blog/understanding-software-dependency-graphs](https://vulncheck.com/blog/understanding-software-dependency-graphs)  
16. 11 best open source tools for Software Architects | Cerbos, accessed June 8, 2025, [https://www.cerbos.dev/blog/best-open-source-tools-software-architects](https://www.cerbos.dev/blog/best-open-source-tools-software-architects)  
17. What is the best way to generate a complete UML class diagram ..., accessed June 8, 2025, [https://community.lambdatest.com/t/what-is-the-best-way-to-generate-a-complete-uml-class-diagram-from-a-java-project-and-how-can-i-visualize-class-relationships-effectively/36354](https://community.lambdatest.com/t/what-is-the-best-way-to-generate-a-complete-uml-class-diagram-from-a-java-project-and-how-can-i-visualize-class-relationships-effectively/36354)  
18. Auto-magically generate sequence diagrams of your code's runtime behavior \- AppMap, accessed June 8, 2025, [https://appmap.io/blog/2022/11/29/automagically-generate-sequence-diagrams-of-your-codes-runtime-behavior/](https://appmap.io/blog/2022/11/29/automagically-generate-sequence-diagrams-of-your-codes-runtime-behavior/)  
19. Automatic generator of UML class diagrams from source code using PlantUML \- GitHub, accessed June 8, 2025, [https://github.com/lorenzovngl/plantuml-generator](https://github.com/lorenzovngl/plantuml-generator)  
20. Build your first AI Agent with ADK \- Agent Development Kit by Google \- DEV Community, accessed June 8, 2025, [https://dev.to/marianocodes/build-your-first-ai-agent-with-adk-agent-development-kit-by-google-409b](https://dev.to/marianocodes/build-your-first-ai-agent-with-adk-agent-development-kit-by-google-409b)  
21. aws.amazon.com, accessed June 8, 2025, [https://aws.amazon.com/what-is/retrieval-augmented-generation/\#:\~:text=Retrieval%2DAugmented%20Generation%20(RAG),sources%20before%20generating%20a%20response.](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval%2DAugmented%20Generation%20\(RAG\),sources%20before%20generating%20a%20response.)  
22. What is Retrieval-Augmented Generation (RAG)? | Google Cloud, accessed June 8, 2025, [https://cloud.google.com/use-cases/retrieval-augmented-generation](https://cloud.google.com/use-cases/retrieval-augmented-generation)  
23. Top 9 Open-Source SAST Tools | Wiz, accessed June 8, 2025, [https://www.wiz.io/academy/top-open-source-sast-tools](https://www.wiz.io/academy/top-open-source-sast-tools)  
24. Use static analysis · binkley/modern-java-practices Wiki \- GitHub, accessed June 8, 2025, [https://github.com/binkley/modern-java-practices/wiki/Use-static-analysis](https://github.com/binkley/modern-java-practices/wiki/Use-static-analysis)  
25. Java Static Code Analysis Tools \- Bitshift, accessed June 8, 2025, [https://www.bitshifted.co/blog/java-static-code-analysis-tools/](https://www.bitshifted.co/blog/java-static-code-analysis-tools/)  
26. Compare Semgrep to SonarQube | Semgrep, accessed June 8, 2025, [https://semgrep.dev/docs/faq/comparisons/sonarqube](https://semgrep.dev/docs/faq/comparisons/sonarqube)  
27. Semgrep vs Sonarqube: which tool fits your code analysis needs? \- BytePlus, accessed June 8, 2025, [https://www.byteplus.com/en/topic/516927](https://www.byteplus.com/en/topic/516927)  
28. Local CLI scans \- Semgrep, accessed June 8, 2025, [https://semgrep.dev/docs/getting-started/cli-oss](https://semgrep.dev/docs/getting-started/cli-oss)  
29. Is there a set of free open-source SAST tools that are a good replacement to Snyk? \- Reddit, accessed June 8, 2025, [https://www.reddit.com/r/devops/comments/1jm6opu/is\_there\_a\_set\_of\_free\_opensource\_sast\_tools\_that/](https://www.reddit.com/r/devops/comments/1jm6opu/is_there_a_set_of_free_opensource_sast_tools_that/)  
30. Article 3 \- OWASP Dependency-Check and Vulnerability Scanning \- adorsys, accessed June 8, 2025, [https://adorsys.com/blog/article-3-owasp-dependency-check-and-vulnerability-scanning/](https://adorsys.com/blog/article-3-owasp-dependency-check-and-vulnerability-scanning/)  
31. Slizaa, accessed June 8, 2025, [http://www.slizaa.org/](http://www.slizaa.org/)  
32. python-call-graph · PyPI, accessed June 8, 2025, [https://pypi.org/project/python-call-graph/](https://pypi.org/project/python-call-graph/)  
33. hpnog/javaDependenceGraph: This tool is a Program ... \- GitHub, accessed June 8, 2025, [https://github.com/hpnog/javaDependenceGraph](https://github.com/hpnog/javaDependenceGraph)  
34. Tools to Generate UML Diagrams from Source Code? : r/softwaredevelopment \- Reddit, accessed June 8, 2025, [https://www.reddit.com/r/softwaredevelopment/comments/1jblnfo/tools\_to\_generate\_uml\_diagrams\_from\_source\_code/](https://www.reddit.com/r/softwaredevelopment/comments/1jblnfo/tools_to_generate_uml_diagrams_from_source_code/)  
35. jfeliu007/goplantuml: PlantUML Class Diagram Generator for golang projects \- GitHub, accessed June 8, 2025, [https://github.com/jfeliu007/goplantuml](https://github.com/jfeliu007/goplantuml)  
36. DOT (graph description language) \- Wikipedia, accessed June 8, 2025, [https://en.wikipedia.org/wiki/DOT\_(graph\_description\_language)](https://en.wikipedia.org/wiki/DOT_\(graph_description_language\))  
37. azixaka/a2adotnet: The Agent2Agent (A2A) protocol implementation for .net. \- GitHub, accessed June 8, 2025, [https://github.com/azixaka/a2adotnet](https://github.com/azixaka/a2adotnet)  
38. Agent2Agent: A practical guide to build agents \- Composio, accessed June 8, 2025, [https://composio.dev/blog/agent2agent-a-practical-guide-to-build-agents/](https://composio.dev/blog/agent2agent-a-practical-guide-to-build-agents/)  
39. Semgrep Guide for a Security Engineer (Part 5 of 6\) | Caesar Creek Software, accessed June 8, 2025, [https://cc-sw.com/semgrep-guide-for-a-security-engineer-part-5-of-6/](https://cc-sw.com/semgrep-guide-for-a-security-engineer-part-5-of-6/)  
40. Interact with Server \- Agent2Agent Protocol (A2A) \- Google, accessed June 8, 2025, [https://google.github.io/A2A/tutorials/python/6-interact-with-server/](https://google.github.io/A2A/tutorials/python/6-interact-with-server/)  
41. Reverse Call Graphs for PowerBuilder, Oracle and SQL Server \- Visual Expert, accessed June 8, 2025, [https://www.visual-expert.com/EN/visual-expert-documentation/code-cross-references/reverse-call-graphs.html](https://www.visual-expert.com/EN/visual-expert-documentation/code-cross-references/reverse-call-graphs.html)  
42. Change impact analysis \- Wikipedia, accessed June 8, 2025, [https://en.wikipedia.org/wiki/Change\_impact\_analysis](https://en.wikipedia.org/wiki/Change_impact_analysis)  
43. How to Use OWASP Dependency Check in a Maven Project, accessed June 8, 2025, [https://www.albinsblog.com/2025/01/how-to-use-owasp-dependency-check-in-maven-projec.html](https://www.albinsblog.com/2025/01/how-to-use-owasp-dependency-check-in-maven-projec.html)
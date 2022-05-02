import java.io.*;
import java.net.Socket;
import java.util.Base64;

public class JavaSocket {

    private String host;
    private int port;
    private Socket socket;
    private OutputStream outputStream;
    private FileInputStream fileInputStream;
    private PrintWriter printWriter;
    private ByteArrayOutputStream byteArrayOutputStream;

    public JavaSocket(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public static void main(String[] args) throws IOException {
        String host = "127.0.0.1";
        int port = 12345;
        String imageName = "/Users/lujiahuan/4projects/yolov5+javaweb/yolov5/images/images_dir/11111.jpg";

        File imageFile = new File(imageName);
        JavaSocket javaSocket = new JavaSocket(host, port);
        javaSocket.createSocketServer(imageFile);
        javaSocket.getServer();
        javaSocket.closeStream();
    }

    // 创建各类stream
    public void createSocketServer(File imageFile) throws IOException {
        this.socket = new Socket(this.host, this.port);
        this.outputStream =  socket.getOutputStream();
        this.fileInputStream = new FileInputStream(imageFile);
        this.byteArrayOutputStream = new ByteArrayOutputStream();
    }

    // 调用python创建的socket服务
    public void getServer() throws IOException {
        int length = 0;
        byte[] sendBytes = new byte[1024 * 20];
        while((length = this.fileInputStream.read(sendBytes, 0, sendBytes.length)) > 0){
            byteArrayOutputStream.write(sendBytes, 0, length);
        }
        byteArrayOutputStream.flush();
        printWriter = new PrintWriter(outputStream);
        printWriter.write(Base64.getEncoder().encodeToString(byteArrayOutputStream.toByteArray()));
        printWriter.flush();
        socket.shutdownOutput();

        InputStream inputStream = socket.getInputStream();
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        String responseInfo = bufferedReader.readLine();
        System.out.println(responseInfo);
    }

    // 关闭各类stream
    public void closeStream () {
        try {
            this.socket.close();
            this.outputStream.close();
            this.fileInputStream.close();
            this.printWriter.close();
            this.byteArrayOutputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
using UnityEngine;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.IO;
using System;
using LitJson;

public class NetworkConfig
{
    public const string SERVER_IP = "127.0.0.1";
    public const int PORT = 10205;
}


public class SensorState
{
    public void SetPacket(PositionPacket data)
    {
        angle = data.angle;
        pos = data.pos;
        isValid = data.isValid;
    }

    public double angle;
    public Vector3 pos;
    public bool isValid;
}

public struct PositionPacket
{
    static public string ByteArrayToString(byte[] data)
    {
        string line = System.Text.Encoding.Default.GetString(data);
        int length = 0;
        for (length = 0; length < line.Length; ++length)
        {
            if (line[length] == '\0')
            {
                break;
            }
        }
        line = line.Substring(0, length);
        return line;
    }

    public static PositionPacket Create(byte[] data)
    {
        var line = ByteArrayToString(data);
        JsonData jsonData = JsonMapper.ToObject(line);

        PositionPacket packet = new PositionPacket();

        double angle = (double)jsonData["angle"];
        Vector3 pos = new Vector3(
            (int)jsonData["index_pos"][0],
            (int)jsonData["index_pos"][1],
            (int)jsonData["index_pos"][2]);
        packet.angle = angle;
        packet.pos = pos;
        return packet;

    }

    public bool isValid;
    public double angle;
    public Vector3 pos;


}

public class SensorClient : MonoBehaviour 
{
    private TcpClient client;
    private Stream stream;

    private SensorState sensor;
    private bool running = false;

    private byte[] sendBuffer = new byte[10];
    private byte[] recvBuffer = new byte[1024];

    private bool readyToRequest = false;

    public void Start ()
    {
        Debug.Log("SensorClient::Start Begin");
        client = new TcpClient(NetworkConfig.SERVER_IP, NetworkConfig.PORT);
        stream = client.GetStream();
        running = true;
        Debug.Log("SensorClient::Start End");

        sensor = new SensorState();
        readyToRequest = true;

        
	}

    public void OnDestroy()
    {
        Debug.Log("SensorClient::On Destory Begin");
        stream.Close();
        client.Close();
        Debug.Log("SensorClient::On Destory End");
    }

    public void OnGUI()
    {
        string msgX = string.Format("x={0}", sensor.pos.x);
        string msgY = string.Format("y={0}", sensor.pos.y);
        string msgZ = string.Format("z={0}", sensor.pos.z);
        string msgAngle = string.Format("angle={0}", sensor.angle);

        GUI.Label(new Rect(10, 10, 100, 20), msgX);
        GUI.Label(new Rect(10, 30, 100, 20), msgY);
        GUI.Label(new Rect(10, 50, 100, 20), msgZ);
        GUI.Label(new Rect(10, 70, 100, 20), msgAngle);
    }
	
	public void Update () 
    {
        if (readyToRequest == true)
        {
            Array.Clear(sendBuffer, 0, sendBuffer.Length);
            stream.BeginWrite(recvBuffer, 0, recvBuffer.Length, new AsyncCallback(SendCallback), sensor);
            readyToRequest = false;
        }
	}

    protected void SendCallback(IAsyncResult ar)
    {
        Array.Clear(recvBuffer, 0, recvBuffer.Length);
        stream.BeginRead(recvBuffer, 0, recvBuffer.Length, new AsyncCallback(RecvCallback), sensor);
    }

    protected void RecvCallback(IAsyncResult ar)
    {
        PositionPacket packet = PositionPacket.Create(recvBuffer);
        sensor.SetPacket(packet);
        readyToRequest = true;
    }
}

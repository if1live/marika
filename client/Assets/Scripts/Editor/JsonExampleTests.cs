using System;
using UnityEngine;
using NUnit.Framework;
using LitJson;

[TestFixture]
[Category("Json Example")]
internal class JsonExampleTests
{
    [Test]
    public void JsonReadTest()
    {
        string data = "{\"angle\": 0.123, \"index_pos\": [42, 54, 44]}";
        JsonData jsonData = JsonMapper.ToObject(data);

        double angle = (double)jsonData["angle"];
        Assert.AreEqual(angle, 0.123, 0.001);

        Assert.AreEqual(42, (int)jsonData["index_pos"][0]);
        Assert.AreEqual(54, (int)jsonData["index_pos"][1]);
        Assert.AreEqual(44, (int)jsonData["index_pos"][2]);
    }

    [Test]
    public void JsonReadNullTest()
    {
        string data = "{\"angle\": null, \"index_pos\": null}";
        JsonData jsonData = JsonMapper.ToObject(data);

        Assert.AreEqual(null, jsonData["angle"]);
        Assert.AreEqual(null, jsonData["index_pos"]);
    }
}


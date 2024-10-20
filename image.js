//sk-DXZKbW1v1_znGWULQqYBfxPqRrNi4KdVwj_DNBunpUT3BlbkFJk4SoZ14PVQ9hktHlKWhloN05BSGxKvwAFMfe3tK_YA
import OpenAI from "openai";

const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,  // Set your OpenAI API key here
});

const openai = new OpenAIApi(configuration);

(async () => {
  const response = await openai.createImage({
    model: "dall-e-3",
    prompt: "a white siamese cat",
    n: 1,
    size: "1024x1024",
  });

  const imageUrl = response.data[0].url;
  console.log("Image URL:", imageUrl);
})();
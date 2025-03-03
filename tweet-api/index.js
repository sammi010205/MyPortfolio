import express from "express";
import pkg from "@prisma/client";
import morgan from "morgan";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(morgan("dev"));

const { PrismaClient } = pkg;
const prisma = new PrismaClient();

// ==== put your endpoints below ====

// Create a Tweet Item
app.post("/tweets", async(req, res) => {
  const {userId, text} = req.body;
  try {
    const newTweet = await prisma.tweet.create({
      data: {
        userId: userId,
        text: text,
      },
    });
    res.status(201).json(newTweet);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


// Delete a Tweet Item by ID
app.delete("/tweets/:id", async(req, res) => {
  const {id} = req.params;
  try {
    const deletedTweet = await prisma.tweet.delete({
      where: {
        id: parseInt(id),
      },
    });
    res.status(200).json(deletedTweet);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


// Get a tweet Item by ID
app.get("/tweets/:id", async(req, res) => {
  const {id} = req.params;
  try {
    const tweet = await prisma.tweet.findUnique({
      where: {
        id: parseInt(id),
      },
    });
    if (tweet) {
      res.status(200).json(tweet);
    }else {
      res.status(404).json({ error: "Tweet not found" });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update a Tweet Item by ID
app.put("/tweets/:id", async(req, res) => {
  const {id} = req.params;
  const {text} = req.body;
  try {
    const updatedTweet = await prisma.tweet.update({
      where: {
        id: parseInt(id),
      },
      data: {
        text: text,
      },
    });
    res.status(200).json(updatedTweet);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


// Get all users sorted by PreferredName
app.get("/users" , async(req, res) => {
  try {
    const users = await prisma.user.findMany({
      orderBy: {
        preferredName: "asc",
      },
    });
    res.status(200).json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


// Create a User Item
app.post("/users", async(req, res) => {
  const {email, name, preferredName} = req.body;
  try {
    const newUser = await prisma.user.create({
      data: {
        email: email,
        name: name,
        preferredName: preferredName,
      },
    });
    res.status(201).json(newUser);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


app.listen(8000, () => {
  console.log("Server running on http://localhost:8000 🎉 🚀");
});

// Prisma Commands
// npx prisma db push: to push the schema to the database or any changes to the schema
// npx prisma studio: to open prisma studio and visualize the database

const mongoose = require("mongoose");

function connectDB(){

    mongoose.connect('mongodb+srv://lakkilakshman12:WpOKni2QVKHJRAFr@rental.x1c06wu.mongodb.net/' , {useUnifiedTopology: true , useNewUrlParser: true})
   

    const connection = mongoose.connection

    connection.on('connected' , ()=>{
        console.log('Mongo DB Connection Successfull')
    })

    connection.on('error' , ()=>{
        console.log('Mongo DB Connection Error')
    })


}

connectDB()

module.exports = mongoose
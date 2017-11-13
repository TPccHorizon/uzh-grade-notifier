import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;


public class UZHGradeNotifier extends JFrame implements ActionListener{

    private JTextField field1 = new JTextField();
    private JPasswordField field2 = new JPasswordField();
    private JTextField field3 = new JTextField();

    private JButton but = new JButton("Start Grade Checking");

    private static String appDir;
    private static String operatingSystem = (System.getProperty("os.name")).toUpperCase();


    public UZHGradeNotifier(){
        super("UZH Grade Notifier");
        setSize(800,500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JPanel p = new JPanel(new BorderLayout());

        p.setLayout(new GridLayout(2,1));


        Box hBox = Box.createVerticalBox();

        Box hBox1 = Box.createHorizontalBox();
        hBox1.add(new JLabel("UZH shortname*"));
        hBox1.add(field1);

        Box hBox2 = Box.createHorizontalBox();
        hBox2.add(new JLabel("Password*"));
        hBox2.add(field2);

        Box hBox3 = Box.createHorizontalBox();
        hBox3.add(new JLabel("Pushbullet token"));
        hBox3.add(field3);


        hBox.add(hBox1);
        hBox.add(hBox2);
        hBox.add(hBox3);


        p.add(hBox);
        but.addActionListener(this);
        p.add(but);

        add(p);

        pack();
        setVisible(true);



        File f = new File(appDir+"/uzh_grade_notifier/version.txt");
        if(!f.exists()) {
            // Download python scripts
        }

    }


    @Override
    public void actionPerformed(ActionEvent e) {
        String str = "{\n    \"username:\":\""+field1.getText()+"\",\n" +
                "    \"password:\":\""+field2.getText()+"\",\n" +
                "    \"pbToken:\":\"" + field3.getText() + "\"\n}";

        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(appDir+"/uzh_grade_notifier/config/config.json"));
            writer.write(str);
            writer.close();

        } catch (IOException e1) {
            e1.printStackTrace();
        }

    }


    public static void main(String[] args){

        if (operatingSystem.contains("WIN")){
            appDir = System.getenv("AppData");
        }else{
            appDir = System.getProperty("user.home");
            appDir += "/Library/Application Support";
        }
        UZHGradeNotifier frame = new UZHGradeNotifier();



    }


}

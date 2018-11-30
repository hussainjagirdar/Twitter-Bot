package LanguageModel;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;


import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocumentList;
import org.apache.solr.common.SolrDocumentList;

public class SolrIngest {
	public static void main(String[] args){
		ingestUsingCSV("test_data.csv"); // insert using csv file
		ingestUsingJSON("test_data.json"); // insert using json file
		ingestUsingJSON("test_doc_J.json"); // insert & update 
		SolrQuery(); // query to solr

	}
	public static void ingestUsingCSV(String file){

		BufferedWriter bw = null;
		FileWriter fw = null;

		ProcessBuilder pb = new ProcessBuilder(
				"curl",
				"--noproxy",
				"127.0.0.1",
				"http://127.0.0.1:8983/solr/testCore/update?commit=true",
				"--data-binary",
				"@"+file,
				"-H",
				"Content-type:application/csv"
				);

		pb.redirectErrorStream(true);

		try
		{
			Process p = pb.start();
			BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));
			String line = null;
			while ( (line = reader.readLine()) != null) {
				System.out.println(line);
			}
		}catch (IOException e){   
			System.out.print("error");
			e.printStackTrace();
		}

	}

	public static void ingestUsingJSON(String file){

		BufferedWriter bw = null;
		FileWriter fw = null;

		ProcessBuilder pb = new ProcessBuilder(
				"curl",
				"--noproxy",
				"127.0.0.1",
				"http://127.0.0.1:8983/solr/testCore/update?commit=true",
				"--data-binary",
				"@"+file,
				"-H",
				"Content-type:application/json"
				);

		pb.redirectErrorStream(true);

		try
		{
			Process p = pb.start();
			BufferedReader reader =  new BufferedReader(new InputStreamReader(p.getInputStream()));
			String line = null;
			while ( (line = reader.readLine()) != null) {
				System.out.println(line);
			}
		}catch (IOException e){   
			System.out.print("error");
			e.printStackTrace();
		}

	}

	public static void SolrQuery(){
		SolrClient client = new HttpSolrClient.Builder("http://127.0.0.1:8983/solr/testCore").build();

		SolrQuery query = new SolrQuery();

		query.setQuery("*:*");
		query.addFilterQuery("phrase:\"computer science\" OR phrase:\"science\"");


		query.setFields("phrase,occurrence_count");

		query.setStart(0);

		query.setRows(100);


		QueryResponse response;
		try {
			response = client.query(query);
			SolrDocumentList results = response.getResults();
			//						System.out.println(results.size());
			for (int i = 0; i < results.size(); ++i) {

				System.out.println(results.get(i).get("phrase").toString()); 

				System.out.println(results.get(i).get("occurrence_count").toString());
				break;


			}
		} catch (SolrServerException | IOException e) {
			e.printStackTrace();
		}

	}


}

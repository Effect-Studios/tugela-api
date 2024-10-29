#![no_std]
use soroban_sdk::{contractimpl, Env, Symbol, Address, Vec, map};

// Define the structure for Freelancer
pub struct Freelancer {
    pub name: Symbol,
    pub wallet: Address,
    pub ownership_percentage: u8, // Percentage of the gig ownership (e.g., 20%)
}

// Define the structure for a Gig
pub struct Gig {
    pub gig_id: Symbol,
    pub client_name: Symbol,
    pub client_address: Address,
    pub freelancers: Vec<Freelancer>,
}

pub struct FreelanceGigNFT;

#[contractimpl]
impl FreelanceGigNFT {
    // Function to create a new gig with fractional ownership
    pub fn create_gig(
        env: Env,
        gig_id: Symbol,
        client_name: Symbol,
        client_address: Address,
        freelancer_names: Vec<Symbol>,
        freelancer_wallets: Vec<Address>,
        ownership_percentages: Vec<u8>,
    ) -> Result<(), Symbol> {
        // Check if input data is consistent
        if freelancer_names.len() != freelancer_wallets.len() || freelancer_names.len() != ownership_percentages.len() {
            return Err(Symbol::new(&env, "Freelancer data mismatch"));
        }

        // Ensure total ownership equals 100%
        let mut total_ownership: u8 = 0;
        for &percentage in ownership_percentages.iter() {
            total_ownership += percentage;
        }
        if total_ownership != 100 {
            return Err(Symbol::new(&env, "Ownership percentages must total 100"));
        }

        // Create a vector of freelancers for the gig
        let mut freelancers = Vec::new(&env);
        for i in 0..freelancer_names.len() {
            let freelancer = Freelancer {
                name: freelancer_names.get(i).unwrap(),
                wallet: freelancer_wallets.get(i).unwrap(),
                ownership_percentage: ownership_percentages.get(i).unwrap(),
            };
            freelancers.push_back(freelancer);
        }

        // Create the gig with the client and freelancers
        let gig = Gig {
            gig_id: gig_id.clone(),
            client_name,
            client_address,
            freelancers,
        };

        // Store the gig in the contract's storage
        env.storage().set(gig_id.clone(), gig);

        Ok(())
    }

    // Function to get gig details by gig_id
    pub fn get_gig(env: Env, gig_id: Symbol) -> Result<Gig, Symbol> {
        if let Some(gig) = env.storage().get::<Symbol, Gig>(gig_id.clone()) {
            return Ok(gig);
        }
        Err(Symbol::new(&env, "Gig not found"))
    }

    // Function to mint fractional NFTs for the freelancers
    pub fn mint_nft(env: Env, gig_id: Symbol) -> Result<(), Symbol> {
        let gig = match env.storage().get::<Symbol, Gig>(gig_id.clone()) {
            Some(g) => g,
            None => return Err(Symbol::new(&env, "Gig not found")),
        };

        // Placeholder for minting NFTs representing fractional ownership
        for freelancer in gig.freelancers.iter() {
            // Logic for minting NFT for each freelancer with ownership percentage
            env.events().publish((Symbol::new(&env, "NFTMinted"), freelancer.name.clone(), freelancer.ownership_percentage));
        }

        Ok(())
    }
}

